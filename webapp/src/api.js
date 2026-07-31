// Thin wrapper around fetch() for talking to the Django backend
// (see app/api_views.py and app/urls.py "API Routes" section).
//
// The backend uses Django's normal session + CSRF cookie auth (LoginAPIView
// calls django.contrib.auth.login(), not a JWT/token scheme), so every
// request needs credentials: 'include' to carry the session cookie, and
// every unsafe request (POST/PUT/DELETE) needs the X-CSRFToken header.

// NOTE: use "localhost", not "127.0.0.1" — see .env.example for why.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? decodeURIComponent(match[2]) : null;
}

// Hits /api/auth/csrf/, which is decorated with @ensure_csrf_cookie on the
// Django side purely so the browser gets a csrftoken cookie to echo back.
export async function ensureCsrfCookie() {
  await fetch(`${API_BASE_URL}/api/auth/csrf/`, { credentials: 'include' });
}

export async function apiFetch(path, options = {}) {
  const method = (options.method || 'GET').toUpperCase();
  const headers = { ...(options.headers || {}) };

  if (!['GET', 'HEAD', 'OPTIONS'].includes(method)) {
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) headers['X-CSRFToken'] = csrftoken;
    if (options.body && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    method,
    headers,
    credentials: 'include',
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    // some endpoints (e.g. logout) may return an empty body
  }

  if (!response.ok) {
    const message = (data && (data.error || data.detail)) || `Request failed (${response.status})`;
    throw new Error(message);
  }
  return data;
}

export const api = {
  csrf: () => ensureCsrfCookie(),
  currentUser: () => apiFetch('/api/auth/user/'),
  login: (username, password) =>
    apiFetch('/api/auth/login/', { method: 'POST', body: JSON.stringify({ username, password }) }),
  logout: () => apiFetch('/api/auth/logout/', { method: 'POST' }),
  products: () => apiFetch('/api/products/'),
  categories: () => apiFetch('/api/categories/'),
  cart: () => apiFetch('/api/cart/'),
  addToCart: (productId) =>
    apiFetch('/api/cart/add/', { method: 'POST', body: JSON.stringify({ product_id: productId }) }),
  incrementCartItem: (cartItemId) =>
    apiFetch(`/api/cart/items/${cartItemId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ action: 'increment' }),
    }),
  decrementCartItem: (cartItemId) =>
    apiFetch(`/api/cart/items/${cartItemId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ action: 'decrement' }),
    }),
  removeCartItem: (cartItemId) => apiFetch(`/api/cart/items/${cartItemId}/`, { method: 'DELETE' }),
};
