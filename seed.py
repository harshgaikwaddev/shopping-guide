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
        ]
    )

    print("Seed data inserted.")


if __name__ == "__main__":
    seed()
