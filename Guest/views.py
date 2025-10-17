from django.shortcuts import render, redirect
from django.http import JsonResponse
from Admin.models import *
from django.contrib.auth.hashers import make_password
import json
from django.contrib.auth.hashers import check_password

from django.views.decorators.csrf import csrf_exempt


def home_view(request):
    return render(request, 'home.html')

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        address = data.get('address')
        password = make_password(data.get('password'))
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        date_of_birth = data.get('date_of_birth')

        user = User.objects.create(
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        )

        return JsonResponse({'message': 'Registration successful'})

    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type')

        if user_type == 'Admin':
            try:
                user = AdminUser.objects.get(username=username)
                if password==user.password:
                    request.session['adin_username'] = user.username
                    return JsonResponse({'message': 'Login successful', 'user_type': 'Admin'})
                else:
                    return JsonResponse({'message': 'Invalid password'})
            except AdminUser.DoesNotExist:
                return JsonResponse({'message': 'Admin not found'})

        elif user_type == 'Sub Admin':
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['username'] = user.username
                    return JsonResponse({'message': 'Login successful', 'user_type': 'Sub Admin'})
                else:
                    return JsonResponse({'message': 'Invalid password'})
            except SubAdmin.DoesNotExist:
                return JsonResponse({'message': 'Sub Admin not found'})

        elif user_type == 'User':
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['username'] = user.username
                    return JsonResponse({'message': 'Login successful', 'user_type': 'User'})
                else:
                    return JsonResponse({'message': 'Invalid password'})
            except User.DoesNotExist:
                return JsonResponse({'message': 'User not found'})

        return JsonResponse({'message': 'Invalid user type'})

    return render(request, 'adminlogin.html')


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *



@api_view(['POST'])
def customer_register(request):
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email_id_customer')
        if CustomerRegTBL.objects.filter(email_id_customer=email).exists():
            return Response({"message": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Customer registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

import fitz  # PyMuPDF for PDF
import docx
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import os

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def owner_register(request):
    serializer = OwnerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email_id_owner')
        if OwnerRegTBL.objects.filter(email_id_owner=email).exists():
            return Response({"message": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        license_file = request.FILES.get('license_document')
        status_flag = 0

        if license_file:
            ext = os.path.splitext(license_file.name)[1].lower()

            # Save the file temporarily to read
            file_path = f"/tmp/{license_file.name}"
            with open(file_path, 'wb+') as destination:
                for chunk in license_file.chunks():
                    destination.write(chunk)

            text = ''
            try:
                if ext == '.pdf':
                    with fitz.open(file_path) as doc:
                        for page in doc:
                            text += page.get_text()
                elif ext == '.docx':
                    doc = docx.Document(file_path)
                    for para in doc.paragraphs:
                        text += para.text + '\n'
            except Exception as e:
                return Response({"message": "Error reading document", "error": str(e)}, status=500)
            finally:
                os.remove(file_path)  # Clean up

            if 'licence number' in text.lower() and 'licency name' in text.lower():
                status_flag = 1

        serializer.save(status=status_flag)
        return Response({"message": "Owner registered successfully.", "status": status_flag}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user_type = request.data.get('user_type')

    if not email or not password or not user_type:
        return Response({'message': 'Email, password, and user_type are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_type = int(user_type)
    except:
        return Response({'message': 'Invalid user_type','type':user_type}, status=status.HTTP_400_BAD_REQUEST)

    if user_type == 1:  # Owner
        try:
            user = OwnerRegTBL.objects.get(email_id_owner=email, password=password)
            if user.status == 1:
                return Response({'message': 'Login successful', 'user_type': 1, 'email': user.email_id_owner, 'name': user.name})
            else:
                return Response({'message': 'Account blocked'}, status=status.HTTP_403_FORBIDDEN)
        except OwnerRegTBL.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    elif user_type == 2:  # Staff
        try:
            user = StaffTBL.objects.get(email_id_staff=email, password=password)
            if user.status == 1:
                return Response({'message': 'Login successful', 'user_type': 2, 'email': user.email_id_staff,'name': user.name,'staff_type': user.staff_type})
            else:
                return Response({'message': 'Account blocked'}, status=status.HTTP_403_FORBIDDEN)
        except StaffTBL.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    elif user_type == 3:  # Customer
        try:
            user = CustomerRegTBL.objects.get(email_id_customer=email, password=password)
            if user.status == 1:
                return Response({'message': 'Login successful', 'user_type': 3, 'email': user.email_id_customer, 'name': user.name})
            else:
                return Response({'message': 'Account blocked'}, status=status.HTTP_403_FORBIDDEN)
        except CustomerRegTBL.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        return Response({'message': 'Invalid user types','type':user_type}, status=status.HTTP_400_BAD_REQUEST)



# views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import random


otp_storage = {}  # Temporary dictionary to store OTPs

def forgot_password(request):
    return render(request, 'forgot_password.html')

def send_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        user_type = request.POST['user_type']
        otp = str(random.randint(100000, 999999))

        user_exists = False

        if user_type == 'customer' and CustomerRegTBL.objects.filter(email_id_customer=email).exists():
            user_exists = True
        elif user_type == 'owner' and OwnerRegTBL.objects.filter(email_id_owner=email).exists():
            user_exists = True
        elif user_type == 'staff' and StaffTBL.objects.filter(email_id_staff=email).exists():
            user_exists = True

        if user_exists:
            otp_storage[email] = otp
            send_mail(
                'OTP for Password Reset',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return render(request, 'reset_password.html', {'email': email, 'user_type': user_type})
        else:
            messages.error(request, 'User not found!')
            return redirect('Guest:forgot_password')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user_type = request.POST['user_type']
        entered_otp = request.POST['otp']
        new_password = request.POST['new_password']

        if otp_storage.get(email) == entered_otp:
            if user_type == 'customer':
                user = CustomerRegTBL.objects.get(email_id_customer=email)
            elif user_type == 'owner':
                user = OwnerRegTBL.objects.get(email_id_owner=email)
            elif user_type == 'staff':
                user = StaffTBL.objects.get(email_id_staff=email)

            user.password = new_password
            user.save()
            del otp_storage[email]
            return render(request, 'success.html', {'message': 'Password changed successfully'})
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('Guest:forgot_password')

