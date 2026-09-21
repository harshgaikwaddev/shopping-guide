import os
from datetime import datetime

from pymongo import MongoClient
from werkzeug.security import generate_password_hash

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "shopping_guide")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]


def seed():
    if db.users.count_documents({}) > 0:
        print("Database already has users. Skipping seed.")
        return

    owner_id = db.users.insert_one(
        {
            "name": "Demo Owner",
            "email": "owner@example.com",
            "password_hash": generate_password_hash("demo1234"),
            "role": "owner",
            "created_at": datetime.utcnow(),
        }
    ).inserted_id

    db.users.insert_one(
        {
            "name": "Demo Customer",
            "email": "customer@example.com",
            "password_hash": generate_password_hash("demo1234"),
            "role": "customer",
            "created_at": datetime.utcnow(),
        }
    )

    shop_id = db.shops.insert_one(
        {
            "owner_id": owner_id,
            "name": "City Electronics",
            "address": "Main Market Road",
            "phone": "9000000000",
            "category": "Electronics",
            "lat": 28.6139,
            "lng": 77.2090,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ).inserted_id

    grocery_owner_id = db.users.insert_one(
        {
            "name": "Grocery Owner",
            "email": "grocery@example.com",
            "password_hash": generate_password_hash("demo1234"),
            "role": "owner",
            "created_at": datetime.utcnow(),
        }
    ).inserted_id

    grocery_shop_id = db.shops.insert_one(
        {
            "owner_id": grocery_owner_id,
            "name": "Fresh Basket",
            "address": "Lake View Street",
            "phone": "9111111111",
            "category": "Grocery",
            "lat": 28.5355,
            "lng": 77.3910,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ).inserted_id

    tech_owner_id = db.users.insert_one(
        {
            "name": "Tech Hub Owner",
            "email": "techhub@example.com",
            "password_hash": generate_password_hash("demo1234"),
            "role": "owner",
            "created_at": datetime.utcnow(),
        }
    ).inserted_id

    tech_shop_id = db.shops.insert_one(
        {
            "owner_id": tech_owner_id,
            "name": "Tech Hub",
            "address": "Innovation Avenue",
            "phone": "9222222222",
            "category": "Computers & Accessories",
            "lat": 28.6280,
            "lng": 77.2195,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ).inserted_id

    gaming_owner_id = db.users.insert_one(
        {
            "name": "Game Zone Owner",
            "email": "gamezone@example.com",
            "password_hash": generate_password_hash("demo1234"),
            "role": "owner",
            "created_at": datetime.utcnow(),
        }
    ).inserted_id

    gaming_shop_id = db.shops.insert_one(
        {
            "owner_id": gaming_owner_id,
            "name": "Game Zone",
            "address": "Stadium Circle",
            "phone": "9333333333",
            "category": "Gaming",
            "lat": 28.6020,
            "lng": 77.2290,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ).inserted_id

    home_owner_id = db.users.insert_one(
        {
            "name": "Home Essentials Owner",
            "email": "homeessentials@example.com",
            "password_hash": generate_password_hash("demo1234"),
            "role": "owner",
            "created_at": datetime.utcnow(),
        }
    ).inserted_id

    home_shop_id = db.shops.insert_one(
        {
            "owner_id": home_owner_id,
            "name": "Home Essentials",
            "address": "Market Square",
            "phone": "9444444444",
            "category": "Home & Furniture",
            "lat": 28.5750,
            "lng": 77.2400,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ).inserted_id

    db.products.insert_many(
        [
            {
                "shop_id": shop_id,
                "name": "Smartphone X1",
                "price": 25999.0,
                "stock": 5,
                "updated_at": datetime.utcnow(),
            },
            {
                "shop_id": shop_id,
                "name": "Bluetooth Headset Pro",
                "price": 2999.0,
                "stock": 2,
                "updated_at": datetime.utcnow(),
            },
            {
                "shop_id": grocery_shop_id,
                "name": "Basmati Rice 5kg",
                "price": 699.0,
                "stock": 18,
                "updated_at": datetime.utcnow(),
            },
            {
                "shop_id": grocery_shop_id,
                "name": "Olive Oil 1L",
                "price": 899.0,
                "stock": 0,
                "updated_at": datetime.utcnow(),
            },
            {
                "shop_id": tech_shop_id,
                "name": "Laptop Desk",
                "price": 3499.0,
                "stock": 7,
                "updated_at": datetime.utcnow(),
            },
            {
                "shop_id": tech_shop_id,
                "name": "Mechanical Keyboard",
                "price": 4299.0,
                "stock": 4,
                "updated_at": datetime.utcnow(),
            },
            {
                "shop_id": gaming_shop_id,
                "name": "Gaming Chair",
                "price": 8999.0,
                "stock": 3,
                "updated_at": datetime.utcnow(),
            },
            {
                "shop_id": gaming_shop_id,
                "name": "Gaming Headphone",
                "price": 2499.0,
                "stock": 9,
                "updated_at": datetime.utcnow(),
            },
            {
                "shop_id": home_shop_id,
                "name": "Foldable Table",
                "price": 2199.0,
                "stock": 6,
                "updated_at": datetime.utcnow(),
            },
        ]
    )

    print("Seed data inserted.")


if __name__ == "__main__":
    seed()
