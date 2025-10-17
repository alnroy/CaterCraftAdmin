from django.shortcuts import render, redirect
from django.http import JsonResponse
from Admin.models import *
from django.contrib.auth.hashers import make_password
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def userdetls(request):
    username = request.session.get('username')
    ob=User.objects.get(username=username)
    return ob


@csrf_exempt
def user_home(request):
    return render(request, 'User/home.html')




def view_profile(request):
    user = userdetls(request)
    return render(request, 'User/view_profile.html', {'user': user})


def edit_profile(request):
    user =userdetls(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.address = data.get('address', user.address)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        if data['date_of_birth']!="":
            user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        user.save()
        return JsonResponse({'message': 'Profile updated successfully'})
    return render(request, 'User/edit_profile.html', {'user': user})



# views.py

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from Admin.models import *
from .serializers import *
from datetime import datetime


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_service(request):
    try:
        rate = request.data.get('rate')
        items = request.data.get('items')
        description = request.data.get('description')
        status_val = 1
        datetime_val = datetime.now()

        email = request.data.get('email_id_owner')
        image = request.FILES.get('image')

        if not OwnerRegTBL.objects.filter(email_id_owner=email).exists():
            return Response({'error': 'Owner not found'}, status=status.HTTP_404_NOT_FOUND)

        owner = OwnerRegTBL.objects.get(email_id_owner=email)

        service = ServiceTBL.objects.create(
            rate=rate,
            items=items,
            description=description,
            status=status_val,
            datetime=datetime_val,
            image=image,
            email_id_owner=owner
        )

        return Response({
            'message': 'Service added successfully',
            'service_id': service.service_id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(['POST'])
def register_staff(request):
    try:
        name = request.data.get('name')
        address = request.data.get('address')
        mob_no = request.data.get('mob_no')
        id_proof = request.data.get('id_proof')
        email_id_staff = request.data.get('email_id_staff')
        email_id_owner = request.data.get('email_id_owner')
        email_id_shop = request.data.get('email_id_shop')  # optional
        password = request.data.get('password')
        upi = request.data.get('upi')
        wage = request.data.get('wage')
        assigned_to = request.data.get('assigned_to')
        staff_type = request.data.get('staff_type')

        # Fetch owner and shop
        try:
            owner = OwnerRegTBL.objects.get(email_id_owner=email_id_owner)
        except OwnerRegTBL.DoesNotExist:
            return Response({'error': 'Owner not found'}, status=status.HTTP_404_NOT_FOUND)

        shop = None
        if email_id_shop:
            try:
                shop = ShopTBL.objects.get(email_id_shop=email_id_shop)
            except ShopTBL.DoesNotExist:
                return Response({'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create staff
        staff = StaffTBL.objects.create(
            name=name,
            address=address,
            mob_no=mob_no,
            id_proof=id_proof,
            email_id_staff=email_id_staff,
            email_id_owner=owner,
            email_id_shop=shop,
            password=password,
            upi=upi,
            wage=wage,
            assigned_to=assigned_to,
            staff_type=staff_type
        )

        return Response({'message': 'Staff registered successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def view_bookings_for_owner(request):
    owner_email = request.data.get('owner_email')

    if not owner_email:
        return Response({'status': 'error', 'message': 'owner_email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        owner = OwnerRegTBL.objects.get(email_id_owner=owner_email)
    except OwnerRegTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Owner not found'}, status=status.HTTP_404_NOT_FOUND)

    services = ServiceTBL.objects.filter(email_id_owner=owner)
    bookings = BookingTBL.objects.filter(service__in=services)

    booking_list = []
    for booking in bookings:
        booking_list.append({
            'id': booking.id,
            'items': booking.items,
            'rate': booking.rate,
            'datetime': booking.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            'approvalStatus': booking.Approvalstatus,
            'paymentStatus': booking.PaymentStatus,
            'workCompletedStatus': booking.WorkCompletedSts,
            'assignedTeam': booking.assigned_team,
            'customerEmail': booking.email_id_customer.email_id_customer
        })

    return Response({'status': 'success', 'bookings': booking_list}, status=status.HTTP_200_OK)


@api_view(['POST'])
def approve_booking(request):
    booking_id = request.data.get('booking_id')
    team = request.data.get('team')

    if not booking_id :
        return Response({'status': 'error', 'message': 'booking_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    if team == 'null':
        return Response({'status': 'error', 'message': 'booking_id is required'}, status=status.HTTP_400_BAD_REQUEST)


    try:
        booking = BookingTBL.objects.get(id=booking_id)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    booking.Approvalstatus = 1  # Assuming 1 means approved
    booking.assigned_team = team
    booking.save()

    return Response({'status': 'success', 'message': 'Booking approved successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reject_booking(request):
    booking_id = request.data.get('booking_id')

    if not booking_id:
        return Response({'status': 'error', 'message': 'booking_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        booking = BookingTBL.objects.get(id=booking_id)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    booking.Approvalstatus = 2  # Assuming 2 means rejected
    booking.save()

    return Response({'status': 'success', 'message': 'Booking rejected successfully'}, status=status.HTTP_200_OK)



@api_view(['POST'])
def view_chat(request):
    booking_id = request.data.get('booking_id')

    if not booking_id:
        return Response({'status': 'error', 'message': 'booking_id is required'}, status=400)

    try:
        booking = BookingTBL.objects.get(id=booking_id)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=404)

    chats = CustOwnerChat.objects.filter(bookingid=booking).order_by('timestamp')

    chat_list = []
    for chat in chats:
        chat_list.append({
            'id': chat.id,
            'message': chat.message,
            'direction': chat.sts,
            'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return Response({'status': 'success', 'chats': chat_list}, status=200)


@api_view(['POST'])
def send_chat(request):
    booking_id = request.data.get('booking_id')
    message = request.data.get('message')
    sts = 2

    if not booking_id or not message or not sts:
        return Response({'status': 'error', 'message': 'booking_id, message and sts are required'}, status=400)

    try:
        booking = BookingTBL.objects.get(id=booking_id)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=404)

    CustOwnerChat.objects.create(
        bookingid=booking,
        message=message,
        sts=int(sts),
        timestamp=timezone.now()
    )

    return Response({'status': 'success', 'message': 'Chat message sent successfully'}, status=201)




@api_view(['POST'])
def view_feedback_for_owner(request):
    owner_email = request.data.get('owner_email')

    if not owner_email:
        return Response({'status': 'error', 'message': 'owner_email is required'}, status=400)

    try:
        owner = OwnerRegTBL.objects.get(email_id_owner=owner_email)
    except OwnerRegTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Owner not found'}, status=404)

    services = ServiceTBL.objects.filter(email_id_owner=owner)
    bookings = BookingTBL.objects.filter(service__in=services)
    feedbacks = FeedbackTBL.objects.filter(bookingid__in=bookings).order_by('-datetime')

    if not feedbacks.exists():
        return Response({'status': 'success', 'feedbacks': [], 'message': 'No feedbacks found for this owner'}, status=200)

    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response({'status': 'success', 'feedbacks': serializer.data}, status=200)


@api_view(['POST'])
def view_staff_by_team(request):
    owner_email = request.data.get('owner_email')
    team_name = request.data.get('team')

    if not owner_email or not team_name:
        return Response({'status': 'error', 'message': 'owner_email and team are required'}, status=400)

    try:
        owner = OwnerRegTBL.objects.get(email_id_owner=owner_email)
    except OwnerRegTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Owner not found'}, status=404)

    staffs = StaffTBL.objects.filter(email_id_owner=owner, assigned_to=team_name)

    staff_list = []
    for staff in staffs:
        staff_list.append({
            'staff_id': staff.email_id_staff,
            'staff_name': staff.name,
            'staff_type': staff.staff_type,
        })

    return Response({'status': 'success', 'staffs': staff_list}, status=200)


@api_view(['POST'])
def view_staff_detail(request):
    staff_id = request.data.get('staff_id')

    if not staff_id:
        return Response({'status': 'error', 'message': 'staff_id is required'}, status=400)

    try:
        staff = StaffTBL.objects.get(email_id_staff=staff_id)
    except StaffTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Staff not found'}, status=404)

    staff_data = {
        'name': staff.name,
        'email_id_staff': staff.email_id_staff,
        'address': staff.address,
        'mob_no': staff.mob_no,
        'id_proof': staff.id_proof,
        'upi': staff.upi,
        'wage': staff.wage,
        'assigned_to': staff.assigned_to,
        'staff_type': staff.staff_type,
        'status': staff.status,
        'email_id_owner': staff.email_id_owner.email_id_owner,
        'email_id_shop': staff.email_id_shop.email_id_shop if staff.email_id_shop else None,
    }

    return Response({'status': 'success', 'staff_details': staff_data}, status=200)




@api_view(['POST'])
def view_service(request):
    owner_email = request.data.get('owner_email')

    if not owner_email :
        return Response({'status': 'error', 'message': 'owner_email and team are required'}, status=400)

    try:
        owner = OwnerRegTBL.objects.get(email_id_owner=owner_email)
    except OwnerRegTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Owner not found'}, status=404)

    services = ServiceTBL.objects.filter(email_id_owner=owner)

    service_list = []

    for service in services:
        service_list.append({
            'id': service.service_id,
            'rate': service.rate,
            'items': service.items,
            'description': service.description,
            'image_url': request.build_absolute_uri(service.image.url) if service.image else None,
            'Company Name': service.email_id_owner.company_name
        })

    return Response({'status': 'success', 'services': service_list}, status=200)


