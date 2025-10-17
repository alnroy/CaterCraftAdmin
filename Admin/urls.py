from django.urls import path
from .views import *

app_name="Admin"


urlpatterns = [
 path('admin_home',admin_home, name='admin_home'),
 path('view_users/', view_all_users, name='view_all_users'),
  path('admin_login/', admin_login, name='admin_login'),
  path('view_feedbacks_admin/', view_feedbacks_admin, name='view_feedbacks_admin'),
  path('view_all_bookings/', view_all_bookings, name='view_all_bookings'),
  path('view_all_owners/', view_all_owners, name='view_all_owners'),
  path('delete_owner/', delete_owner, name='delete_owner'),
  path('get_all_customers/', get_all_customers, name='get_all_customers'),





path('admin/home/', admin_home, name='adminhome'),

    path('profile/', profile, name='profile'),
    path('customers/', view_customers, name='view_customers'),
    path('owners/', view_owners, name='view_owners'),
    path('feedbacks/', view_feedbacks, name='view_feedbacks'),
    path('customers/remove/<str:email>/', remove_customer, name='remove_customer'),
    path('owners/approve/<str:email>/', approve_owner, name='approve_owner'),
    path('owners/reject/<str:email>/', reject_owner, name='reject_owner'),
    path('owners/remove/<str:email>/', remove_owner, name='remove_owner'),


]
