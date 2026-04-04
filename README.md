# LezzShop - AI-Powered E-Commerce Platform

<div align="center">

![LezzShop](https://img.shields.io/badge/LezzShop-E--Commerce-purple?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-5.2+-green?style=for-the-badge&logo=django)
![AI Powered](https://img.shields.io/badge/AI-Gemini%20LLM-blue?style=for-the-badge&logo=google)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python)
![Render](https://img.shields.io/badge/Render-Ready-00d4aa?style=for-the-badge&logo=render)
![Stripe](https://img.shields.io/badge/Stripe-Integrated-635bff?style=for-the-badge&logo=stripe)

**Shopping Made Easy with Genie!** 🧞🛍️✨

A modern, full-stack e-commerce platform featuring AI-powered product recommendations, intelligent chatbot assistance, and automated price monitoring.

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots)

</div>

---

## 📝 Project Description

**LezzShop** is a modern e-commerce platform built with Django 5.2+ and integrated with Google's Gemini LLM for AI-powered product recommendations and conversational shopping assistance.

**Key Capabilities:**
- 🤖 AI chatbot ("Genie") for intelligent product search and personalized recommendations using Google Generative AI
- 💰 Real-time price alerts with email notifications, auto-buy functionality, and asynchronous task processing via Celery
- 🎨 Modern responsive UI with product slideshow, hierarchical categories, and seamless cart integration

---

## 🌟 Features

### 🤖 AI-Powered Shopping Assistant
- **Genie Chatbot**: Real-time conversational AI powered by Google's Gemini LLM
- **Smart Product Search**: Natural language queries like "Show me laptops under ₹50000"
- **Personalized Recommendations**: AI analyzes queries to suggest relevant products
- **Recipe Shopping**: Ask for recipes and get matching product recommendations
- **Keyword Intelligence**: Advanced keyword matching with fuzzy search capabilities

### 💰 Smart Price Monitoring System
- **Price Alerts**: Set target prices and get email notifications when prices drop
- **Auto-Buy Feature**: Automatically add products to cart when target price is reached
- **Async Processing**: Celery-based background task processing for efficient monitoring
- **Email Notifications**: Gmail SMTP integration for reliable alert delivery
- **Price History**: Track price changes over time

### 🎨 Modern User Interface
- **Product Slideshow**: Eye-catching automatic carousel showcasing featured products
- **Responsive Design**: Perfect experience on mobile, tablet, and desktop
- **Gradient Themes**: Beautiful purple gradient design throughout
- **Smooth Animations**: Engaging transitions and hover effects
- **Clean Layout**: Intuitive navigation and user-friendly interface

### 🛒 Complete Shopping Experience
- **Shopping Cart**: Full cart management with quantity controls
- **Hierarchical Categories**: Easy browsing with nested product categories
- **Product Details**: Comprehensive product pages with images and descriptions
- **User Authentication**: Secure login, registration, and profile management
- **Order Management**: Track purchases and order history

### 📧 Notification System
- **Email Alerts**: Automated price drop notifications
- **Real-time Updates**: Instant notifications when deals are available
- **Custom Thresholds**: Set personalized price targets

### 🔐 Security & Performance
- **Django Authentication**: Built-in secure user authentication
- **CSRF Protection**: Cross-site request forgery protection
- **Password Hashing**: Secure password storage
- **Session Management**: Secure session handling
- **Async Tasks**: Non-blocking background processing

---

## 🛠️ Tech Stack

### Backend Technologies
- **Django 5.2+** - Python web framework for rapid development
- **Python 3.8+** - Core programming language
- **Celery** - Distributed task queue for asynchronous processing
- **SQLite** - Development database (PostgreSQL-ready for production)
- **Django ORM** - Object-relational mapping for database operations

### AI & Machine Learning
- **Google Generative AI** - Gemini LLM for intelligent chatbot
- **rapidfuzz** - Fuzzy string matching for intelligent search
- **Natural Language Processing** - Query understanding and intent recognition

### Frontend Technologies
- **Bootstrap 5** - Responsive CSS framework
- **JavaScript (ES6+)** - Client-side interactivity
- **AJAX** - Asynchronous data loading for smooth UX
- **HTML5/CSS3** - Modern semantic markup and styling
- **Font Awesome** - Icon library

### Additional Libraries
- **Pillow** - Python Imaging Library for image processing
- **python-dotenv** - Environment variable management
- **django-celery-results** - Task result backend
- **django-celery-beat** - Periodic task scheduler
- **gunicorn** - Production WSGI server
- **whitenoise** - Static file serving for production
- **psycopg2** - PostgreSQL database adapter
- **dj-database-url** - Database URL parsing
- **Stripe** - Payment processing integration

### Development Tools
- **Git** - Version control
- **pip** - Python package manager
- **Virtual Environment** - Isolated Python environment

---

## 📦 Installation

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Google Gemini API Key ([Get it here](https://ai.google.dev/))
- Gmail account (for email notifications)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/saumya1317/lezzshop.git
cd lezzshop
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the project root (see `.env.example` for all options):

```env
# Django Settings
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Gemini AI API
GEMINI_API_KEY=your_gemini_api_key_here

# Email Configuration (Gmail)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password

# Stripe (Testing)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# CORS and CSRF (for frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000

# Database (optional for production)
DATABASE_URL=postgresql://user:password@localhost/dbname
```

**Getting Gmail App Password:**
1. Go to Google Account settings
2. Enable 2-Step Verification
3. Generate App Password for "Mail"
4. Use that password in `.env`

#### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow prompts to create admin account.

#### 7. Collect Static Files
```bash
python manage.py collectstatic
```

#### 8. Start Development Server
```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000/`

#### 9. Start Celery Worker (For Price Alerts)

In a **separate terminal**:
```bash
# Activate virtual environment first
celery -A ecommerce worker -l info
```

---

## 🚀 Usage

### Accessing the Application

- **Homepage**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **AI Assistant**: `http://127.0.0.1:8000/assistant/`

### Using the AI Assistant (Genie)

Try these example queries:

**Product Search:**
- "Show me laptops under ₹50000"
- "I need a wedding outfit under ₹5000"
- "Casual wear for women"
- "Smartphones under ₹20000"

**Recipe Shopping:**
- "Recipe for pasta under ₹200"
- "How to make pizza under ₹500"
- "Cook chicken curry under ₹300"

**General Queries:**
- "I need jeans"
- "Show me ethnic wear"
- "Affordable electronics"

### Setting Price Alerts

1. Navigate to any product detail page
2. Scroll to "Price Alert" section
3. Enter your target price
4. (Optional) Check "Buy automatically" for auto-purchase
5. Click "Set Alert"
6. Receive email when price drops!

### Admin Panel Features

Login at `/admin/` to:
- Add/Edit/Delete Products
- Manage Categories
- View Orders
- Monitor Price Alerts
- Manage Users

---

## 📁 Project Structure

```
lezzshop/
├── app/                          # Main Django application
│   ├── migrations/              # Database migrations
│   ├── static/app/              # Static files (CSS, JS, images)
│   │   ├── css/
│   │   │   ├── style.css       # Custom styles
│   │   │   └── owl.carousel.min.css
│   │   └── js/
│   │       └── myscript.js     # Custom JavaScript
│   ├── templates/app/           # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Homepage
│   │   ├── assistant.html      # AI Chatbot page
│   │   ├── productdetail.html  # Product details
│   │   ├── addtocart.html      # Shopping cart
│   │   └── ...                 # Other templates
│   ├── admin.py                # Admin panel configuration
│   ├── models.py               # Database models
│   ├── views.py                # View functions & AI logic
│   ├── urls.py                 # URL routing
│   ├── forms.py                # Django forms
│   └── tasks.py                # Celery tasks
├── ecommerce/                   # Project configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── celery.py               # Celery configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── media/                       # User-uploaded files
│   └── products_new/           # Product images
├── staticfiles/                 # Collected static files
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore file
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔧 Configuration

### Django Settings

Key settings in `ecommerce/settings.py`:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379'  # or your broker
CELERY_RESULT_BACKEND = 'django-db'
```

### Database Configuration

**Development (SQLite):**
Already configured by default.

**Production (PostgreSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lezzshop_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🎯 How It Works

### 1. AI-Powered Shopping Assistant

**Architecture:**
```
User Query → Keyword Extraction → Category Matching → Product Filter → Display Results
```

**Implementation Highlights:**
- Uses keyword-based matching for reliability
- Fuzzy string matching with rapidfuzz for flexibility
- Fallback to Gemini LLM for complex queries
- Real-time AJAX for instant responses

**Code Flow:**
```python
# views.py - Simplified
def handle_product_query(user_query, model):
    # Extract category from query
    category = extract_category(user_query)
    
    # Extract budget
    budget = extract_budget(user_query)
    
    # Query database
    products = Product.objects.filter(
        category=category,
        discounted_price__lte=budget
    )
    
    # Return formatted HTML
    return render_product_cards(products)
```

### 2. Smart Price Monitoring System

**Architecture:**
```
Price Change → Celery Task → Check Alerts → Send Email → Auto-Buy (if enabled)
```

**Implementation Highlights:**
- Celery for async background processing
- Django signals for price change detection
- Gmail SMTP for notifications
- Atomic database transactions

**Code Flow:**
```python
# tasks.py - Simplified
@shared_task
def process_price_alert(alert_id, new_price):
    alert = PriceAlert.objects.get(id=alert_id)
    
    if new_price <= alert.target_price:
        # Send email notification
        send_email(alert.user, alert.product)
        
        # Auto-buy if enabled
        if alert.buy_when_drop:
            Cart.objects.create(user=alert.user, product=alert.product)
        
        alert.fulfilled = True
        alert.save()
```

---

## 🧪 Testing

### Manual Testing

1. **Test AI Chatbot:**
   - Navigate to `/assistant/`
   - Try various queries
   - Verify product recommendations

2. **Test Price Alerts:**
   - Create alert on product
   - Change product price in admin
   - Verify email notification

3. **Test Shopping Cart:**
   - Add products to cart
   - Update quantities
   - Test checkout flow

### Running Tests (if available)
```bash
python manage.py test
```

---

## 📊 Database Models

### Key Models

**Product Model:**
```python
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='products_new')
```

**PriceAlert Model:**
```python
class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    target_price = models.FloatField()
    buy_when_drop = models.BooleanField(default=False)
    fulfilled = models.BooleanField(default=False)
```

---

## 🚢 Deployment

### 🎯 Deploying on Render (Recommended)

This project is fully configured for production deployment on Render with PostgreSQL, static files, and Stripe.

**Quick Start:**
1. Read [DEPLOYMENT.md](DEPLOYMENT.md) for complete step-by-step instructions
2. Connect your GitHub repository to Render
3. Set environment variables in Render dashboard
4. Deploy automatically on push

**What's Included:**
- ✅ `Procfile` - Render process definitions
- ✅ `runtime.txt` - Python version specification  
- ✅ Environment-based configuration in `settings.py`
- ✅ WhiteNoise middleware for static file serving
- ✅ Automatic database migrations on deploy
- ✅ Production security settings (SSL, HSTS, CSP)
- ✅ PostgreSQL database support
- ✅ Stripe webhook configuration

### Production Checklist

- [ ] Generate secure SECRET_KEY (see DEPLOYMENT.md)
- [ ] Set `DEBUG=False` environment variable
- [ ] Configure PostgreSQL database URL
- [ ] Set up Stripe live keys (if payments needed)
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Set CORS_ALLOWED_ORIGINS for frontend
- [ ] Configure email credentials
- [ ] Set up Stripe webhooks
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Test locally with `DEBUG=False` before deploying

### Local Production Testing

```bash
# Test with production settings locally
DEBUG=False python manage.py runserver

# Collect static files
python manage.py collectstatic --noinput

# Run with gunicorn (like Render does)
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
```

### Deployment with Gunicorn

```bash
# Install gunicorn (included in requirements.txt)
pip install gunicorn

# Run server
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker (Optional)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Celery not starting**
```bash
# Solution: Install and start Redis
# Windows: Download from https://github.com/microsoftarchive/redis/releases
# Linux: sudo apt-get install redis-server
# Mac: brew install redis
```

**Issue: Email not sending**
```bash
# Solution: Check Gmail App Password
# Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env
```

**Issue: AI not responding**
```bash
# Solution: Verify GEMINI_API_KEY in .env
# Get key from https://ai.google.dev/
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Saumya Rai**
- GitHub: [@saumya1317](https://github.com/saumya1317)
- Project: LezzShop - Shopping Made Easy with Genie!

---

## 🙏 Acknowledgments

- **Google Gemini** for AI capabilities
- **Django Community** for excellent documentation
- **Bootstrap** for responsive design framework
- **Font Awesome** for beautiful icons
- **Celery** for task queue system

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Your Email]
- Documentation: Check this README

---

## � Payment Processing with Stripe

Stripe integration is configured and ready for use:

**Features:**
- ✅ Secure payment processing
- ✅ Webhook handling for payment confirmations
- ✅ Test and live mode support
- ✅ Environment-based key management

**Setup:**
1. Create Stripe account at [stripe.com](https://stripe.com)
2. Get API keys from dashboard
3. Add to environment variables:
   - `STRIPE_PUBLIC_KEY` (test or live)
   - `STRIPE_SECRET_KEY` (test or live)
   - `STRIPE_WEBHOOK_SECRET` (webhook signing secret)
4. Configure webhook endpoints in Stripe dashboard

---

## 📈 Future Enhancements

Planned features:
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Order tracking system  
- [ ] Complete payment checkout flow
- [ ] Social authentication (Google, Facebook)
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Live chat support
- [ ] Product comparison feature

---

<div align="center">

**Made with ❤️ by Saumya Rai**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/saumya1317/lezzshop/issues) • [Request Feature](https://github.com/saumya1317/lezzshop/issues)

</div>
