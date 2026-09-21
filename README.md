Shopping Guide MVP

Overview
- Two user roles: customer and owner
- Customers search products, compare shops, and view nearby inventory
- Owners register shops and manage product stock and pricing

Setup
1) Create and activate a Python environment.
2) Install dependencies: pip install -r requirements.txt
3) Start MongoDB locally.
4) **IMPORTANT - Database Isolation:**
   - Copy `.env.example` to `.env`
   - Change `MONGO_DB_NAME` to a unique name (e.g., `shopping_guide_dev` or `shopping_guide_teammate`)
   - This ensures your test data stays separate from others
5) Seed demo data: python seed.py
6) Run the app: python app.py

Demo Accounts
- Owner: owner@example.com / demo1234
- Customer: customer@example.com / demo1234

Notes
- Customers can search, filter in-stock items, and sort by price or distance.
- Owners can add, edit, and delete products from their shop.
- Each developer should use a different MONGO_DB_NAME in their .env to avoid data conflicts

---

## Copyright & License

**Copyright © 2026 - Harsh Satish Gaikwad. All rights reserved.**

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

- ✅ You can use this project
- ✅ You can modify for personal/educational use
- ❌ You cannot claim ownership
- ❌ You cannot remove copyright notice
- ❌ You cannot sell without permission

**Unauthorized copying, distribution, or commercial use without explicit permission is prohibited.**
