# Django Deployment Guide - Render

This guide walks you through deploying this Django application on Render with Stripe and static files fully configured.

## Prerequisites

- Render account (free tier available)
- Git repository with this code
- Environment variables configured

## Step 1: Set Up Render Web Service

1. Go to [render.com](https://render.com)
2. Create a new PostgreSQL database:
   - Name: `django-shopping-db`
   - Region: Choose closest to you
   - Note the `DATABASE_URL` - you'll need it

3. Create a new Web Service:
   - Connect your GitHub repository
   - Select the repository
   - Name: `django-shopping` (or your choice)
   - Environment: Python 3
   - Region: Same as database
   - Branch: `main` (or your default)
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start command: `gunicorn ecommerce.wsgi`

## Step 2: Configure Environment Variables

In Render dashboard, go to your Web Service → Environment:

Add the following variables:

```
DEBUG=False
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=your-app-name.onrender.com

# Database (Render provides this automatically, but verify it's set)
DATABASE_URL=<from Render PostgreSQL database>

# CORS and CSRF Settings
CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com,https://yourfrontenddomain.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com,https://yourfrontenddomain.com

# Email Configuration
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-google-app-password

# Stripe (Use Live Keys in Production)
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# API Keys
GEMINI_API_KEY=your-gemini-api-key

# Celery/Redis (if using Celery)
CELERY_BROKER_URL=<redis-url-if-needed>
CELERY_RESULT_BACKEND=<redis-url-if-needed>
```

### Generating a SECRET_KEY

Run this command in Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Then paste the output into Render's `SECRET_KEY` variable.

## Step 3: Configure Stripe Webhooks

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint:
   - URL: `https://your-app-name.onrender.com/api/stripe-webhook/`
   - Events: Select `payment_intent.succeeded`, `charge.refunded`, etc.
3. Copy the webhook signing secret
4. Add to Render environment variables as `STRIPE_WEBHOOK_SECRET`

## Step 4: Static Files (WhiteNoise)

WhiteNoise is already configured in `settings.py`. During deployment:

1. The build command runs `python manage.py collectstatic --noinput`
2. WhiteNoise serves collected static files automatically
3. No additional configuration needed

To test locally:
```bash
python manage.py collectstatic --noinput
```

## Step 5: Database Migrations

Migrations run automatically via the `release` command in `Procfile`:
```
release: python manage.py migrate
```

If migrations fail, SSH into your Render instance and run manually:
```bash
python manage.py migrate
```

## Step 6: Deploy

### First Deployment
1. Push changes to GitHub
2. Render automatically detects push and deploys
3. Watch deployment logs in Render dashboard
4. Check "Logs" tab for any errors during build/migration

### Subsequent Deployments
Just push to your repository and Render redeploys automatically.

## Troubleshooting

### Static Files Not Loading
- Check Render logs for `collectstatic` errors
- Verify `STATIC_ROOT` is set in settings
- Ensure `whitenoise` middleware is in MIDDLEWARE list

### Database Connection Issues
- Verify `DATABASE_URL` environment variable is set
- Check database credentials are correct
- Ensure database service is available

### Stripe Payments Not Working
- Verify Stripe keys are correct (test vs. live)
- Check webhook endpoint is configured
- Review Stripe webhook delivery logs
- Ensure `STRIPE_WEBHOOK_SECRET` matches Render env var

### CORS/CSRF Errors
- Update `CORS_ALLOWED_ORIGINS` with your frontend domain
- Update `CSRF_TRUSTED_ORIGINS` with your frontend domain
- Ensure protocol is `https` (not http)

### Memory Issues
- Upgrade to Paid Render instance if needed
- Disable unnecessary apps in `INSTALLED_APPS`
- Reduce logging verbosity in production

## Production Security Checklist

- [ ] SECRET_KEY is secure and unique
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configured correctly
- [ ] SSL/HTTPS enforced (Render does this by default)
- [ ] Database password is strong
- [ ] Stripe keys are in LIVE mode (not test)
- [ ] Email credentials configured correctly
- [ ] CORS_ALLOWED_ORIGINS matches your frontend
- [ ] Webhooks properly secured
- [ ] Regular backups enabled in Render

## Helpful Commands

Connect to Render shell:
```bash
# Available in Render dashboard under Web Service
```

View logs:
```bash
# Check Render dashboard Logs tab
```

Manual migration:
```bash
python manage.py migrate
```

Create superuser:
```bash
python manage.py createsuperuser
```

## Monitoring

1. Render Dashboard: Monitor resource usage
2. Stripe Dashboard: Monitor payment events
3. Django Admin: Monitor database records
4. Email: Check if emails are sending correctly

## References

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [Stripe Webhooks](https://stripe.com/docs/webhooks)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

