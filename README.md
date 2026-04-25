# Kartavya Solar 🌞

A modern, responsive e-commerce platform for solar energy products built with Django 6.0, featuring a clean design system, secure authentication, and seamless user experience.

![Kartavya Solar](https://img.shields.io/badge/Django-6.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **🔐 Secure Authentication**: OTP-based email verification and Google OAuth integration
- **🛒 E-commerce Functionality**: Product catalog, shopping cart, and checkout system
- **💳 Payment Integration**: Razorpay payment gateway support
- **📱 Responsive Design**: Mobile-first approach with modern UI/UX
- **🎨 Clean Design System**: Consistent typography, colors, and components
- **⚡ Performance Optimized**: Fast loading with optimized assets
- **🔒 Security First**: Environment-based configuration and secure practices

## 🛠️ Tech Stack

### Backend

- **Django 6.0** - Web framework
- **PostgreSQL** - Database
- **Redis** - Caching (optional)
- **Celery** - Background tasks

### Frontend

- **TailwindCSS 4** - Utility-first CSS framework
- **Django Tailwind** - Django integration
- **Lucide Icons** - Modern icon library
- **Plus Jakarta Sans** - Typography

### Authentication & Payments

- **Django Allauth** - Social authentication
- **Google OAuth 2.0** - Social login
- **Razorpay** - Payment processing

### Development Tools

- **Django Browser Reload** - Hot reloading
- **Django Crispy Forms** - Form rendering
- **Django Unfold** - Admin interface enhancement

## 🎨 Design System

### Color Palette

- **Primary**: Orange (`#f97316`) - Energy and warmth
- **Secondary**: Slate (`#64748b`) - Professional and clean
- **Accent**: Emerald (`#10b981`) - Success and growth
- **Background**: Slate-50 (`#f8fafc`) - Clean and minimal

### Typography

- **Font Family**: Plus Jakarta Sans (400, 600, 700, 800)
- **Headings**: Bold weights with tight letter spacing
- **Body**: Regular weight with optimal readability
- **Navigation**: Small caps with increased letter spacing

### Components

- **Buttons**: Rounded corners with hover animations
- **Cards**: Subtle shadows and clean borders
- **Forms**: Crispy forms with Tailwind styling
- **Navigation**: Sticky header with backdrop blur
- **Icons**: Lucide icon set for consistency

### Layout Principles

- **Mobile-First**: Responsive design starting from mobile
- **Grid System**: Max-width containers with proper spacing
- **Whitespace**: Generous use of space for breathing room
- **Animations**: Smooth transitions and micro-interactions

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Node.js 18+ (for TailwindCSS)
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/mayanknanera/Kartavya-Solar.git
   cd Kartavya-Solar
   ```

2. **Create virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration
DB_NAME=kartavya_solar
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Social Authentication (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Payment Gateway (Optional)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
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
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

## 🎯 Usage

### Development

```bash
# Run development server
python manage.py runserver

# Run with auto-reload
python manage.py tailwind runserver

# Create database migrations
python manage.py makemigrations

# Run tests
python manage.py test
```

### Production Deployment

```bash
# Collect static files
python manage.py collectstatic

# Use production settings
export DJANGO_SETTINGS_MODULE=config.settings.production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Community** - For the excellent web framework
- **TailwindCSS** - For the utility-first CSS framework
- **Lucide** - For the beautiful icon set
- **Google Fonts** - For Plus Jakarta Sans typography

## 📞 Support

For support, email support@kartavyasolar.com or join our Discord community.

---

**Built with ❤️ for a sustainable future**
