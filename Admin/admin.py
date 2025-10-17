from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *  # Import your model

admin.site.register(AdminUser)

admin.site.register(OwnerRegTBL)
admin.site.register(ShopTBL)
admin.site.register(StaffTBL)
admin.site.register(CustomerRegTBL)
admin.site.register(ServiceTBL)
admin.site.register(BookingTBL)
admin.site.register(CustOwnerChat)
admin.site.register(FeedbackTBL)
admin.site.register(ManagerStaffChat)
