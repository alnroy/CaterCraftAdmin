from .views import *
from django.urls import path

app_name="Guest"

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logins', login_view, name='logins'),
    path('', home_view, name='home'),
    path('register-customer/', customer_register, name='customer-register'),
    path('register-owner/', owner_register, name='owner-register'),
    path('login/', login_user, name='login_user'),

    path('forgot-password/', forgot_password, name='forgot_password'),
    path('send-otp/', send_otp, name='send_otp'),
    path('reset-password/', reset_password, name='reset_password'),


]
