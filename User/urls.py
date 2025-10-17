from django.urls import path
from .views import *

app_name="User"


urlpatterns = [
path('user_home', user_home, name='user_home'),
path('profile/', view_profile, name='view_profile'),
path('profile/edit/', edit_profile, name='edit_profile'),
path('add-service/', add_service, name='add-service'),
path('register-staff/', register_staff, name='register_staff'),
path('view-bookings/', view_bookings_for_owner, name='view-bookings'),
path('approve-booking/', approve_booking,name='approve-booking'),
path('reject_booking/', reject_booking,name='reject_booking'),
path('view_chat/', view_chat,name='view_chat'),
path('send_chat/', send_chat,name='send_chat'),
path('view_feedback_for_owner/', view_feedback_for_owner,name='view_feedback_for_owner'),
path('view_staff_by_team/', view_staff_by_team,name='view_staff_by_team'),
path('view_staff_detail/', view_staff_detail,name='view_staff_detail'),
path('view_service/', view_service,name='view_service'),

]
