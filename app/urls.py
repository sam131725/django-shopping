from django.urls import path
from . import views
from .views import home, CategoryView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
from .views import logout_view
from . import api_views

urlpatterns = [
    path('', home, name='home'),
    path('about/' , views.about , name = "about"),

    path('contact/' , views.contact, name = "contact"),
    path('contact/', views.contact_view, name='contact-view'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
   
    path('category/<path:val>/', CategoryView.as_view(), name='category'),

    path('category/', CategoryView.as_view(), name='category_redirect'),

    path("category-title/<val>/" , views.CategoryTitle.as_view(), name= "category-title"),
    path("product-detail/<int:pk>/",views.ProductDetail.as_view(),name="product-detail"),
    path("product-detail/<int:pk>/price-alert/", views.set_price_alert, name="set_price_alert"),
    path('registration/', views.CustomerRegistrationView.as_view() , name = "CustomerRegistration"),
    path('account/login/', views.user_login , name = 'login'),
    path('accounts/login/', views.user_login , name = 'accounts-login'),  # Django default login URL
    path('address/',views.address, name='address'),
    path('updateaddress/<int:pk>/', views.updateAdress.as_view() , name ="updateaddress"),
     path('logout/', logout_view, name='logout'),
    path('add-to-cart/' , views.add_to_cart,name="add-to-cart"),
    path('buy-now/' , views.buy_now, name='buy-now'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.show_cart,name='checkout'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('search/', views.search, name='search'),
   #path('password-reset/',auth_view.PasswordResetForm.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/password_change.html',form_class=MyPasswordChangeForm,success_url ='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

   path('password-reset/', 
     auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), 
     name='password_reset'),

path('password-reset/done/', 
     auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), 
     name='password_reset_done'),

path('password-reset-confirm/<uidb64>/<token>/', 
     auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), 
     name='password_reset_confirm'),

path('password-reset-complete/', 
     auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), 
     name='password_reset_complete'),

path('assistant/', views.assistant, name='assistant'),

# Stripe Payment Routes
path('stripe-checkout/', views.checkout_view, name='stripe-checkout'),
path('payment-success/', views.payment_success_view, name='payment-success'),
path('payment-cancel/', views.payment_cancel_view, name='payment-cancel'),
path('stripe-webhook/', views.stripe_webhook_view, name='stripe-webhook'),
path('order-history/', views.order_history_view, name='order-history'),
path('order-detail/<int:order_id>/', views.order_detail_view, name='order-detail'),

# API Routes
path('api/products/', api_views.ProductListAPIView.as_view(), name='api-products'),
path('api/categories/', api_views.CategoryListAPIView.as_view(), name='api-categories'),
path('api/cart/', api_views.CartAPIView.as_view(), name='api-cart'),
path('api/auth/csrf/', api_views.CSRFTokenAPIView.as_view(), name='api-csrf'),
path('api/auth/login/', api_views.LoginAPIView.as_view(), name='api-login'),
path('api/auth/logout/', api_views.LogoutAPIView.as_view(), name='api-logout'),
path('api/auth/user/', api_views.UserAPIView.as_view(), name='api-user'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

