# Kartavya Solar 🌞

A Django e-commerce platform for solar energy products with OTP email verification, Google OAuth, shopping cart, and Cash on Delivery checkout.

![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Tests](https://img.shields.io/badge/tests-101%20passing-brightgreen.svg)

## Tech Stack

- **Backend** — Django 6.0, Python 3.12, SQLite
- **Frontend** — TailwindCSS 4, Lucide Icons
- **Auth** — django-allauth, Google OAuth 2.0, OTP via Gmail SMTP

## Features

- OTP email verification on signup
- Google OAuth login
- Product catalog with search, filter & sort (7 categories, 18 products)
- Shopping cart with quantity controls
- Cash on Delivery checkout with stock management
- Order history & cancellation
- Profile management

## Setup

```bash
# 1. Clone & install
git clone https://github.com/mayanknanera/Kartavya-Solar.git
cd Kartavya-Solar
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Fill in SECRET_KEY, EMAIL_*, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# 3. Database & seed
python manage.py migrate
python manage.py createsuperuser
python manage.py add_products

# 4. Run
python manage.py runserver
```

> For Google OAuth, create an OAuth 2.0 Client ID at [console.cloud.google.com](https://console.cloud.google.com) and add `http://127.0.0.1:8000/accounts/google/login/callback/` as an authorised redirect URI.
