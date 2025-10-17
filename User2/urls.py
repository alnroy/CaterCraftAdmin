from django.urls import path
from .views import *


app_name="User2"

urlpatterns = [
#path('', views.home, name='home')
path('staff-team-bookings/', staff_team_bookings, name='staff_team_bookings'),
path('mark-work-done/', mark_work_done, name='mark_work_done'),
path('my_team_mates/', get_staff_for_booking, name='my_team_mates'),
path('send_chat_message/', send_chat_message, name='send_chat_message'),
path('fetch_chat_messages/', fetch_chat_messages, name='fetch_chat_messages'),
path('my_earnings/', my_earnings, name='my_earnings'),



]
