# Kartavya Solar 🌞

A modern e-commerce platform for solar energy products built with Django 6.0, featuring OTP email verification, Google OAuth, a full shopping cart, and Cash on Delivery checkout.

![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4-blue.svg)
![Tests](https://img.shields.io/badge/tests-101%20passing-brightgreen.svg)

## Features

- **Authentication** — Email + OTP verification, Google OAuth via django-allauth
- **Product Catalog** — 18 products across 7 categories with search, filter, and sort
- **Shopping Cart** — Add, update, remove items; pending cart survives login redirect
- **Checkout** — Cash on Delivery with stock validation and automatic stock deduction
- **Order Management** — Order history, detail view, and cancellation with stock restore
- **Profile** — Update personal info, address, and change password
- **Contact Form** — Sends enquiry emails via SMTP
- **Admin Panel** — Full Django admin with custom branding
- **101 Tests** — Full test coverage across models, forms, utils, and views

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0, Python 3.12 |
| Database | SQLite (dev) |
| Auth | django-allauth, Google OAuth 2.0 |
| Frontend | TailwindCSS 4, Lucide Icons, Plus Jakarta Sans |
| Email | Gmail SMTP |
| Testing | Django TestCase |

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+ (for Tailwind CSS compilation)
- Git

### 1. Clone & install

```bash
git clone https://github.com/mayanknanera/Kartavya-Solar.git
cd Kartavya-Solar

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=Kartavya Solar <your-email@gmail.com>

# Google OAuth (get from Google Cloud Console)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Optional: path to npm (defaults to 'npm')
NPM_BIN_PATH=npm
```

### 3. Set up the database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Seed products

```bash
python manage.py add_products
```

This loads 18 products across all 7 categories (Solar Panels, Inverters, Batteries, Water Heaters, Mounting Structures, Accessories, Cleaning Systems).

### 5. Run the server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials
2. Create an **OAuth 2.0 Client ID** (Web application)
3. Add `http://127.0.0.1:8000/accounts/google/login/callback/` as an authorised redirect URI
4. Copy the Client ID and Secret into your `.env`

The `Site` record required by allauth is created automatically by the database migration — no manual admin setup needed.

## Running Tests

```bash
python manage.py test accounts core --verbosity=2
```

**101 tests** covering:

| Area | Tests |
|---|---|
| CustomUser model | 7 |
| OTP utilities (generate, verify, expiry) | 9 |
| SignupForm validation | 9 |
| Auth views (signup, login, logout, OTP) | 15 |
| Product model & views | 15 |
| Cart (add, update, remove, clear) | 18 |
| Checkout & order flow | 9 |
| Order management (list, cancel) | 6 |
| Static pages & access control | 4 |

## Project Structure

```
solar-project/
├── accounts/                  # Auth app
│   ├── models.py              # CustomUser (email-based login, OTP fields)
│   ├── views.py               # signup, login, OTP verify, logout, password reset
│   ├── forms.py               # SignupForm, LoginForm
│   ├── utils.py               # OTP generation, email sending, verification
│   ├── adapters.py            # Allauth adapter (post-OAuth cart redirect)
│   ├── signals.py             # Social login: mark email verified, process pending cart
│   ├── urls.py                # Auth routes + 4-step password reset
│   └── tests.py               # 42 tests
│
├── core/                      # Main app
│   ├── models.py              # Product, Cart, CartItem, Order, OrderItem
│   ├── views.py               # All product, cart, checkout, order views
│   ├── urls.py                # All routes
│   ├── context_processors.py  # Cart item count injected into every template
│   ├── signals.py             # Auto-create cart on user registration
│   ├── admin.py               # Product, Cart, Order admin
│   └── tests.py               # 59 tests
│
├── core/management/commands/
│   └── add_products.py        # Seed command: 18 products across 7 categories
│
├── config/
│   ├── settings.py            # All Django settings
│   ├── urls.py                # Root URL config
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/                 # All HTML templates
│   ├── base.html              # Shared layout (navbar, messages, footer)
│   ├── home.html
│   ├── about.html
│   ├── contact.html
│   ├── profile.html
│   ├── accounts/              # login, signup, OTP, password reset templates
│   ├── products/              # product_list, product_detail
│   ├── cart/                  # cart
│   ├── checkout/              # checkout
│   └── orders/                # orders, order_detail, order_success
│
├── media/products/            # Uploaded product images
├── .env.example               # Environment variable template
├── .gitignore
├── manage.py
└── requirements.txt
```

## Product Categories

| Category | Products |
|---|---|
| Solar Panels | 400W Poly, 540W Mono, 650W Bifacial |
| Inverters | 3kW On-Grid, 5kW Hybrid, 10kW Three-Phase |
| Batteries | 100Ah Tubular, 150Ah Tubular, 200Ah Lithium-Ion |
| Water Heaters | 200L, 300L |
| Mounting Structures | Galvanized Steel, Aluminium Tin-Shed |
| Accessories | DC Cable, 60A MPPT Controller, MC4 Connectors |
| Cleaning Systems | Automatic Sprinkler, Manual Cleaning Kit |

## Common Commands

```bash
# Run development server
python manage.py runserver

# Run all tests
python manage.py test accounts core

# Seed products
python manage.py add_products

# Create new migrations after model changes
python manage.py makemigrations

# Open Django shell
python manage.py shell
```

---

Built with ❤️ for a sustainable future
