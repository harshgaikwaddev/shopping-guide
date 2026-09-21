"""
Shopping Guide MVP - Main Application
Copyright (c) 2026 - Harsh Satish Gaikwad. All rights reserved.
Licensed under MIT License - See LICENSE file for details.
Unauthorized copying, distribution, or modification is prohibited.
"""

import os
import re
from datetime import datetime
from functools import wraps
from math import radians, sin, cos, asin, sqrt

from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "shopping_guide")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

if os.getenv("SEED_DEMO_DATA", "").lower() == "true":
    from seed import seed

    seed()

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_id, name, email, role):
        self.id = user_id
        self.name = name
        self.email = email
        self.role = role

    @staticmethod
    def from_doc(doc):
        if not doc:
            return None
        return User(
            str(doc["_id"]),
            doc.get("name", ""),
            doc.get("email", ""),
            doc.get("role", "customer"),
        )


@login_manager.user_loader
def load_user(user_id):
    user_obj_id = to_object_id(user_id)
    if not user_obj_id:
        return None
    doc = db.users.find_one({"_id": user_obj_id})
    return User.from_doc(doc)


def to_object_id(value):
    try:
        return ObjectId(value)
    except Exception:
        return None


def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def role_required(role):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash("Access denied for this area.", "danger")
                return redirect(url_for("index"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return r * c


def search_products(query, in_stock_only, sort, user_lat, user_lng, radius_km):
    match = {"name": {"$regex": re.escape(query), "$options": "i"}}
    if in_stock_only:
        match["stock"] = {"$gt": 0}

    results = []
    for product in db.products.find(match):
        shop = db.shops.find_one({"_id": product.get("shop_id")})
        if not shop:
            continue
        distance = None
        if (
            user_lat is not None
            and user_lng is not None
            and shop.get("lat") is not None
            and shop.get("lng") is not None
        ):
            distance = haversine_km(user_lat, user_lng, shop["lat"], shop["lng"])
            if radius_km is not None and distance > radius_km:
                continue
        results.append({"product": product, "shop": shop, "distance_km": distance})

    if sort == "price":
        results.sort(key=lambda r: r["product"].get("price", 0))
    elif sort == "distance":
        results.sort(
            key=lambda r: r["distance_km"] if r["distance_km"] is not None else float("inf")
        )
    elif sort == "stock":
        results.sort(key=lambda r: r["product"].get("stock", 0), reverse=True)
    return results


@app.template_filter("money")
def money(value):
    if value is None:
        return "-"
    return f"{value:,.2f}"


@app.template_filter("km")
def km(value):
    if value is None:
        return "N/A"
    return f"{value:.1f} km"


def get_owner_shop():
    owner_id = to_object_id(current_user.id)
    if not owner_id:
        return None
    return db.shops.find_one({"owner_id": owner_id})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "customer")

        if not name or not email or not password:
            flash("Please fill out all required fields.", "warning")
            return render_template("signup.html")

        if role not in {"customer", "owner"}:
            role = "customer"

        existing = db.users.find_one({"email": email})
        if existing:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for("login"))

        db.users.insert_one(
            {
                "name": name,
                "email": email,
                "password_hash": generate_password_hash(password),
                "role": role,
                "created_at": datetime.utcnow(),
            }
        )
        flash("Signup successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user_doc = db.users.find_one({"email": email})
        if not user_doc or not check_password_hash(user_doc.get("password_hash", ""), password):
            flash("Invalid credentials.", "danger")
            return render_template("login.html")

        login_user(User.from_doc(user_doc))
        flash("Welcome back.", "success")
        if user_doc.get("role") == "owner":
            return redirect(url_for("owner_dashboard"))
        return redirect(url_for("customer_dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("index"))


@app.route("/customer")
@login_required
@role_required("customer")
def customer_dashboard():
    query = request.args.get("q", "").strip()
    sort = request.args.get("sort", "price")
    in_stock = request.args.get("in_stock") == "on"
    nearby = request.args.get("nearby") == "on"
    lat = parse_float(request.args.get("lat"))
    lng = parse_float(request.args.get("lng"))
    radius = parse_float(request.args.get("radius")) if nearby else None

    results = []
    if query:
        results = search_products(query, in_stock, sort, lat, lng, radius)

    return render_template(
        "customer.html",
        results=results,
        query=query,
        sort=sort,
        in_stock=in_stock,
        nearby=nearby,
        lat=lat,
        lng=lng,
        radius=radius,
    )


@app.route("/shop/<shop_id>")
@login_required
@role_required("customer")
def shop_detail(shop_id):
    shop_obj_id = to_object_id(shop_id)
    if not shop_obj_id:
        flash("Shop not found.", "warning")
        return redirect(url_for("customer_dashboard"))

    shop = db.shops.find_one({"_id": shop_obj_id})
    if not shop:
        flash("Shop not found.", "warning")
        return redirect(url_for("customer_dashboard"))

    products = list(db.products.find({"shop_id": shop["_id"]}).sort("name", 1))
    return render_template("shop_detail.html", shop=shop, products=products)


@app.route("/owner", methods=["GET", "POST"])
@login_required
@role_required("owner")
def owner_dashboard():
    shop = get_owner_shop()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()
        category = request.form.get("category", "").strip()
        lat = parse_float(request.form.get("lat"))
        lng = parse_float(request.form.get("lng"))

        if not name or not address:
            flash("Shop name and address are required.", "warning")
            return redirect(url_for("owner_dashboard"))

        shop_data = {
            "owner_id": to_object_id(current_user.id),
            "name": name,
            "address": address,
            "phone": phone,
            "category": category,
            "lat": lat,
            "lng": lng,
            "updated_at": datetime.utcnow(),
        }

        if shop:
            db.shops.update_one({"_id": shop["_id"]}, {"$set": shop_data})
            flash("Shop updated.", "success")
        else:
            shop_data["created_at"] = datetime.utcnow()
            db.shops.insert_one(shop_data)
            flash("Shop registered.", "success")

        return redirect(url_for("owner_dashboard"))

    products = []
    if shop:
        products = list(db.products.find({"shop_id": shop["_id"]}).sort("name", 1))

    return render_template("owner.html", shop=shop, products=products)


@app.route("/owner/product/new", methods=["GET", "POST"])
@login_required
@role_required("owner")
def owner_product_new():
    shop = get_owner_shop()
    if not shop:
        flash("Register your shop before adding products.", "warning")
        return redirect(url_for("owner_dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price = parse_float(request.form.get("price"))
        stock = parse_int(request.form.get("stock"))

        if not name or price is None or price < 0 or stock is None or stock < 0:
            flash("Please provide name, price, and stock.", "warning")
            return render_template("owner_product_form.html", product=None, mode="new")

        db.products.insert_one(
            {
                "shop_id": shop["_id"],
                "name": name,
                "price": price,
                "stock": stock,
                "updated_at": datetime.utcnow(),
            }
        )
        flash("Product added.", "success")
        return redirect(url_for("owner_dashboard"))

    return render_template("owner_product_form.html", product=None, mode="new")


@app.route("/owner/product/<product_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("owner")
def owner_product_edit(product_id):
    shop = get_owner_shop()
    if not shop:
        flash("Register your shop before editing products.", "warning")
        return redirect(url_for("owner_dashboard"))

    product_obj_id = to_object_id(product_id)
    if not product_obj_id:
        flash("Product not found.", "warning")
        return redirect(url_for("owner_dashboard"))

    product = db.products.find_one({"_id": product_obj_id, "shop_id": shop["_id"]})
    if not product:
        flash("Product not found.", "warning")
        return redirect(url_for("owner_dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price = parse_float(request.form.get("price"))
        stock = parse_int(request.form.get("stock"))

        if not name or price is None or price < 0 or stock is None or stock < 0:
            flash("Please provide name, price, and stock.", "warning")
            return render_template("owner_product_form.html", product=product, mode="edit")

        db.products.update_one(
            {"_id": product["_id"]},
            {
                "$set": {
                    "name": name,
                    "price": price,
                    "stock": stock,
                    "updated_at": datetime.utcnow(),
                }
            },
        )
        flash("Product updated.", "success")
        return redirect(url_for("owner_dashboard"))

    return render_template("owner_product_form.html", product=product, mode="edit")


@app.route("/owner/product/<product_id>/delete", methods=["POST"])
@login_required
@role_required("owner")
def owner_product_delete(product_id):
    shop = get_owner_shop()
    if not shop:
        flash("Register your shop before deleting products.", "warning")
        return redirect(url_for("owner_dashboard"))

    product_obj_id = to_object_id(product_id)
    if not product_obj_id:
        flash("Product not found.", "warning")
        return redirect(url_for("owner_dashboard"))

    db.products.delete_one({"_id": product_obj_id, "shop_id": shop["_id"]})
    flash("Product deleted.", "info")
    return redirect(url_for("owner_dashboard"))


if __name__ == "__main__":
    app.run(debug=False)
