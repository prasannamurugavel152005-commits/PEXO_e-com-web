# Pexo Market

Pexo Market is a Django storefront for a small multi-category retailer. It includes a responsive product catalog, search and category filters, session-based shopping cart, customer accounts, product reviews, checkout, order history, and Django admin CRUD for products, categories, customers, reviews, and orders. Product prices and checkout totals are shown in Indian rupees (INR).

## Run locally

From the project root in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py load_demo_data
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the shop and `http://127.0.0.1:8000/admin/` for product and order management. The demo catalog provides 40 sample products across four departments, with 10 products in each. Delivery costs ₹49, and orders of ₹999 or more ship free. The demo catalog uses externally hosted Unsplash product photos; replace the image URLs in admin with your own assets when ready.

## Checks

```powershell
python manage.py test
python manage.py check
```

## Notes

- SQLite is configured by default. `db.sqlite3` is created by migrations and is excluded from version control.
- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, and `DJANGO_ALLOWED_HOSTS` in the deployment environment before production use. The built-in development key is not suitable for deployment.
- Checkout currently supports cash on delivery; it does not process online payments.
- Product/category CRUD and order status management are available through Django admin.