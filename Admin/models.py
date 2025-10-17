from django.db import models

# Create your models here.
class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)
    def __str__(self):
        return self.username


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username



class CustomerRegTBL(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    mob_no = models.CharField(max_length=20)
    id_proof = models.TextField()
    email_id_customer = models.EmailField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    status = models.IntegerField(default=1)  # 1 = Active, 0 = Blocked

    def __str__(self):
        return self.name


class OwnerRegTBL(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    mob_no = models.CharField(max_length=20)
    email_id_owner = models.EmailField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    status = models.IntegerField(default=0)  # 1 = Active, 0 = Blocked
    license_document = models.FileField(upload_to='licenses/',null=True,blank=True)  # Upload path: MEDIA_ROOT/licenses/
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name


class ShopTBL(models.Model):
    upi = models.CharField(max_length=30, unique=True)
    shop_name = models.CharField(max_length=50)
    mob_no = models.CharField(max_length=20)
    status = models.IntegerField()  # 1 = Active, 0 = Blocked
    address = models.CharField(max_length=50)
    id_proof = models.CharField(max_length=50)
    email_id_shop = models.EmailField(max_length=50, primary_key=True)

    def __str__(self):
        return self.shop_name



class StaffTBL(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    mob_no = models.CharField(max_length=20)
    id_proof = models.TextField()

    email_id_staff = models.EmailField(max_length=50, primary_key=True)

    email_id_owner = models.ForeignKey(
        OwnerRegTBL,
        on_delete=models.CASCADE,
    )
    email_id_shop = models.ForeignKey(
        ShopTBL,
        on_delete=models.CASCADE,
        null=True,blank=True
    )

    password = models.CharField(max_length=50)
    status = models.IntegerField(default=1)  # 1 = Active, 0 = Blocked
    upi = models.CharField(max_length=30)
    wage = models.FloatField()
    assigned_to = models.CharField(max_length=20) # Team A, Team B ,Team C ,Team D ,Team E
    staff_type = models.CharField(max_length=20) # 1- manager , 2- chef, 3-Designer , 4-Delivery Agents , 5-Catering boys , 6- local worker

    def __str__(self):
        return f"{self.name} ({self.staff_type})"


class ServiceTBL(models.Model):
    service_id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    rate = models.FloatField()
    items = models.CharField(max_length=50)
    description = models.TextField()
    status = models.IntegerField()  # 1 = Active, 0 = Blocked
    datetime = models.DateTimeField()
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)

    email_id_owner = models.ForeignKey(
        OwnerRegTBL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.items} - ₹{self.rate}"


class BookingTBL(models.Model):
    service = models.ForeignKey(
        ServiceTBL,
        on_delete=models.CASCADE,
    )
    datetime = models.DateTimeField()
    items = models.CharField(max_length=50,null=True,blank=True)
    rate = models.FloatField(null=True)
    Approvalstatus = models.IntegerField(default=0)  # 1 = Approved, 0 = Rejeted
    PaymentStatus=models.IntegerField(default=0)  # 1 = done, 0 = not done
    WorkCompletedSts=models.IntegerField(default=0,)  # 1 = done, 0 = not done
    assigned_team = models.CharField(max_length=50,null=True,blank=True) # Team A, Team B ,Team C ,Team D ,Team E
    email_id_customer = models.ForeignKey(
        CustomerRegTBL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Booking: {self.items} - ₹{self.rate}"


from django.utils import timezone

class CustOwnerChat(models.Model):
    bookingid = models.ForeignKey(
        BookingTBL,
        on_delete=models.CASCADE    )
    message = models.CharField(max_length=500)
    sts = models.IntegerField()  # 1 = Customer to Owner, 2 = Owner to Customer
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        direction = 'Customer → Owner' if self.sts == 1 else 'Owner → Customer'
        return f'{self.bookingid} | {direction} | {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'



class FeedbackTBL(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    email_id_customer = models.ForeignKey(
        CustomerRegTBL,
        on_delete=models.CASCADE
    )
    bookingid = models.ForeignKey(
    BookingTBL,
    on_delete=models.CASCADE    )
    feedback = models.TextField()
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback by {self.email_id_customer.email_id_customer} on {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}"

class ManagerStaffChat(models.Model):
    bookingid = models.ForeignKey(
        BookingTBL,
        on_delete=models.CASCADE    )
    message = models.CharField(max_length=500)
    sts = models.IntegerField()  # 1 = Manager to staff 2- staff to manager
    staff_type = models.CharField(max_length=20) #  opposite staff id 2- chef, 3-Designer , 4-Delivery Agents , 5-Catering boys , 6- local worker
    timestamp = models.DateTimeField(default=timezone.now)
    staff_email =models.CharField(max_length=80) #


