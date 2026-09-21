# Shopping Guide

> Find what you need nearby, compare local prices, and make a more informed purchase.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-local-47A248?style=flat-square&logo=mongodb&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)

Shopping Guide is a local-first marketplace prototype for discovering products in nearby shops. Customers can search inventory, compare prices and stock, and narrow results by distance. Shop owners get a simple dashboard for registering their store and keeping product information current.

## What You Can Do

### For customers

- Search products by name across registered shops
- Show only products that are currently in stock
- Sort results by price, distance, or available stock
- Use browser location or enter coordinates manually
- Filter results to a chosen radius in kilometres
- Open a shop detail page and browse its inventory

### For shop owners

- Create or update a shop profile
- Add products with prices and stock quantities
- Edit product information as inventory changes
- Remove products that are no longer available

## How It Works

```text
Customer                          Shop owner
   |                                  |
   v                                  v
Search local inventory          Register a shop
   |                                  |
   v                                  v
Compare price, stock,          Maintain products,
and distance                   prices, and stock
   |                                  |
   +-------------> Visit the shop <---+
```

Search results are calculated from MongoDB inventory records. When coordinates are available, the app uses the Haversine formula to calculate shop distance and apply the nearby filter.

## Tech Stack

- **Backend:** Python, Flask, Flask-Login
- **Database:** MongoDB through PyMongo
- **Frontend:** Jinja templates, Bootstrap 5, vanilla JavaScript
- **Authentication:** Session-based login with Werkzeug password hashing

## Quick Start

### Prerequisites

- Python 3.10 or newer
- MongoDB running locally on its default port (`27017`)

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure the application

Copy `.env.example` to `.env` and update the values when needed:

```dotenv
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=shopping_guide_dev
SECRET_KEY=replace-with-a-random-secret
```

Use a unique `MONGO_DB_NAME` for each local checkout or developer. This keeps test and seed data isolated when several environments use the same MongoDB server.

### 4. Seed the demo database

```powershell
python seed.py
```

The seed script creates two demo shops, four products, and customer/owner accounts. It skips seeding when the selected database already contains users.

### 5. Run the app

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

On Windows, `start.ps1` can start MongoDB and the Flask app together when MongoDB is installed at `C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe`.

## Demo Accounts

| Role | Email | Password |
| --- | --- | --- |
| Customer | `customer@example.com` | `demo1234` |
| Owner | `owner@example.com` | `demo1234` |
| Owner | `grocery@example.com` | `demo1234` |
| Owner | `techhub@example.com` | `demo1234` |
| Owner | `gamezone@example.com` | `demo1234` |
| Owner | `homeessentials@example.com` | `demo1234` |

## Project Layout

```text
Shopping-Guide/
├── app.py                 # Flask routes, auth, search, and business logic
├── seed.py                # Demo users, shops, and product inventory
├── start.ps1              # Windows MongoDB + Flask launcher
├── requirements.txt       # Python dependencies
├── templates/             # Jinja pages for customers and owners
├── static/                # Frontend JavaScript and styles
└── data/db/               # Local MongoDB files (ignored by Git)
```

## Configuration Notes

- `.env` is ignored by Git and should never contain committed secrets.
- Change the default Flask `SECRET_KEY` before deploying beyond local development.
- Browser geolocation requires permission and works best from a secure context or local development URL.
- The bundled demo passwords are for development only.

## License

This project is available under the [MIT License](LICENSE).

Copyright (c) 2026 Harsh Satish Gaikwad.
