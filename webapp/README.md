# LezzShop web app (React)

A starter React frontend for the existing `django-shopping` REST API
(`app/api_views.py`). This is a separate project — it does not replace the
Django templates, it's a second, independent client that talks to the same
backend over `/api/...`.

## What's here

- Login (session-based, via `/api/auth/login/` + CSRF cookie)
- Product listing (`/api/products/`), with an "Add to Cart" button
- Full cart management (`/api/cart/`, `/api/cart/add/`, `/api/cart/items/<id>/`):
  add, increment, decrement (auto-removes the line at 0), and remove

The three cart-mutation endpoints are new additions to `app/api_views.py` /
`app/urls.py` — they didn't exist when this scaffold was first put together
(the old `plus_cart`/`minus_cart`/`remove_cart` views only served the Django
templates). They're covered by an in-repo functional check (add, increment,
decrement-to-delete, cross-user isolation, anonymous rejection) run via
Django's test client before being wired up here.

## Running it

1. Start the Django backend on `localhost` (not `127.0.0.1` — see
   `.env.example` for why this matters for cookies):
   ```bash
   python manage.py runserver localhost:8000
   ```
2. In this folder:
   ```bash
   npm install
   cp .env.example .env
   npm run dev
   ```
3. Open http://localhost:3000 — Django's `CORS_ALLOWED_ORIGINS` and
   `CSRF_TRUSTED_ORIGINS` already whitelist this exact origin, so no backend
   config changes are needed to try it.
4. Log in with an account created via `/registration/` or `/admin/` on the
   Django side (there's no signup screen here yet).

## What's intentionally left out (next steps)

- Checkout/Stripe flow
- Registration screen
- Category filtering / search
- Price alerts UI

## Talking to production

Set `VITE_API_BASE_URL` in `.env` to the deployed backend's HTTPS URL, and
add this app's deployed origin to `CORS_ALLOWED_ORIGINS` /
`CSRF_TRUSTED_ORIGINS` in `ecommerce/settings.py` (or via the `.env`-driven
env vars it already supports).
