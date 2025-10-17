from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.hashers import make_password
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def admin_home(request):
    return render(request, 'adminhome.html')

def view_all_users(request):
    users = User.objects.all()
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            if user.is_active:
                user.is_active = False
                user.save()
            else:
                user.is_active = True
                user.save()
            return JsonResponse({'message': 'User blocked successfully'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'})
    return render(request, 'Admin/admin_viewusers.html', {'users': users})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email == 'admin@gmail.com' and password == 'admin':
        return Response({
            'status': 'success',
            'message': 'Admin login successful',
            'admin': {
                'name': 'Admin',
                'email': email
            }
        }, status=status.HTTP_200_OK)

    return Response({
        'status': 'error',
        'message': 'Invalid email or password'
    }, status=status.HTTP_401_UNAUTHORIZED)




from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import FeedbackAdminViewSerializer

@api_view(['GET'])
def view_feedbacks_admin(request):
    feedbacks = FeedbackTBL.objects.select_related(
        'email_id_customer', 'bookingid__service__email_id_owner'
    ).all()
    serializer = FeedbackAdminViewSerializer(feedbacks, many=True)
    return Response({
        'status': 'success',
        'feedbacks': serializer.data
    })



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookingViewSerializer

@api_view(['GET'])
def view_all_bookings(request):
    bookings = BookingTBL.objects.select_related(
        'service__email_id_owner', 'email_id_customer'
    ).all()
    serializer = BookingViewSerializer(bookings, many=True)
    return Response({
        'status': 'success',
        'bookings': serializer.data
    })




from .serializers import OwnerDetailSerializer

@api_view(['GET'])
def view_all_owners(request):
    owners = OwnerRegTBL.objects.all()
    serializer = OwnerDetailSerializer(owners, many=True, context={'request': request})
    return Response({
        'status': 'success',
        'owners': serializer.data
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

@api_view(['DELETE'])
def delete_owner(request):
    email_id_owner = request.data.get('email_id_owner')

    if not email_id_owner:
        return Response({
            'status': 'error',
            'message': 'Email ID of the owner is required.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        owner = OwnerRegTBL.objects.get(email_id_owner=email_id_owner)
        owner_name = owner.name
        owner_email = owner.email_id_owner

        # Send email before deletion
        send_mail(
            subject='Account Removal Notification',
            message=f'Dear {owner_name},\n\nYour account has been removed from the system. If you believe this is a mistake, please contact support.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[owner_email],
            fail_silently=False,
        )

        owner.delete()

        return Response({
            'status': 'success',
            'message': f'Owner with email {email_id_owner} deleted and notified successfully.'
        }, status=status.HTTP_200_OK)

    except OwnerRegTBL.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Owner not found.'
        }, status=status.HTTP_404_NOT_FOUND)


from .serializers import CustomerRegTBLSerializer  # Assuming you have a serializer for the model

@api_view(['GET'])
def get_all_customers(request):
    try:
        # Fetch all customer records
        customers = CustomerRegTBL.objects.all()

        # Serialize the customer data
        serializer = CustomerRegTBLSerializer(customers, many=True)

        # Return the serialized data
        return Response({
            'status': 'success',
            'customers': serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





def profile(request):

    try:
        admin = AdminUser.objects.first()
    except AdminUser.DoesNotExist:
        return render(request, 'profile.html',{'admin': 0})


    return render(request, 'profile.html',{'admin': admin})

def view_customers(request):
    customers = CustomerRegTBL.objects.filter(status=1)
    return render(request, 'view_customers.html', {'customers': customers})

def remove_customer(request, email):
    try:
        customer = CustomerRegTBL.objects.get(email_id_customer=email)
        customer.status = 0  # Soft delete (block)
        customer.save()

        # Send notification email
        send_mail(
            subject='Account Deactivation Notice',
            message=f'Dear {customer.name},\n\nYour customer account has been removed (deactivated) from our system. '
                    f'If you believe this was done in error, please contact our support team.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer.email_id_customer],
            fail_silently=False,
        )

    except CustomerRegTBL.DoesNotExist:
        pass

    return redirect('Admin:view_customers')


def view_owners(request):
    owners = OwnerRegTBL.objects.all()
    return render(request, 'view_owners.html', {'owners': owners})

def approve_owner(request, email):
    try:
        owner = OwnerRegTBL.objects.get(email_id_owner=email)
        owner.status = 1
        owner.save()
    except OwnerRegTBL.DoesNotExist:
        pass
    return redirect('Admin:view_owners')

def reject_owner(request, email):
    try:
        owner = OwnerRegTBL.objects.get(email_id_owner=email)
        owner.status = 2
        owner.save()
    except OwnerRegTBL.DoesNotExist:
        pass
    return redirect('Admin:view_owners')

def remove_owner(request, email):
    try:
        owner = OwnerRegTBL.objects.get(email_id_owner=email)
        owner.delete()
    except OwnerRegTBL.DoesNotExist:
        pass
    return redirect('Admin:view_owners')

def view_feedbacks(request):
    feedbacks = FeedbackTBL.objects.select_related('email_id_customer', 'bookingid').all().order_by('-datetime')
    return render(request, 'view_feedbacks.html', {'feedbacks': feedbacks})

