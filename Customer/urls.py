from django.urls import path
from .views import *


app_name="Customer"

urlpatterns = [
    path('view-customer-profile/',view_customer_profile, name='view_customer_profile'),
    path('update-customer-profile/', update_customer_profile, name='update_customer_profile'),
    path('view-all-services/', view_all_services, name='view_all_services'),
    path('book-service/', book_service, name='book_service'),
    path('view-my-bookings/', view_my_bookings, name='view_my_bookings'),
    path('view_chat/', view_chat, name='view_chat'),
    path('send_chat/', send_chat, name='send_chat'),
    path('make-payment/', make_payment, name='make_payment'),
    path('give-feedback/', give_feedback, name='give_feedback'),

]
