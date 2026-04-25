# Kartavya Solar 🌞

A modern e-commerce platform for solar energy products built with Django 6.0, featuring secure authentication, payment integration, and clean design.

![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4+-blue.svg)

## ✨ Features

- 🔐 **Secure Authentication**: OTP email verification & Google OAuth
- 🛒 **E-commerce**: Product catalog, shopping cart, checkout
- 💳 **Payment Integration**: Razorpay gateway support
- 📱 **Responsive Design**: Mobile-first with modern UI/UX
- 🎨 **Clean Design**: Consistent typography & components
- ⚡ **Performance**: Optimized assets & fast loading

## 🛠️ Tech Stack

**Backend**: Django 6.0, PostgreSQL, Redis  
**Frontend**: TailwindCSS 4, Lucide Icons, Plus Jakarta Sans  
**Auth & Payments**: Django Allauth, Google OAuth, Razorpay

## 🚀 Quick Start

### Prerequisites

- Python 3.12+, PostgreSQL 15+, Node.js 18+, Git

### Installation

1. **Clone & Setup**

   ```bash
   git clone https://github.com/mayanknanera/Kartavya-Solar.git
   cd Kartavya-Solar
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Setup**

   ```bash
   cp .env.example .env
   # Edit .env with your database and email credentials
   ```

3. **Database & Run**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

### Environment Variables

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=kartavya_solar
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

## 📁 Project Structure

```
kartavya-solar/
├── accounts/              # User authentication & profiles
├── config/                # Django settings & configuration
├── core/                  # Main application logic
├── media/                 # User uploaded files
├── staticfiles/           # Static assets
├── templates/             # HTML templates
├── theme/                 # TailwindCSS theme
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 🎯 Usage

```bash
# Development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Run tests
python manage.py test
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for a sustainable future**
