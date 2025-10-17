from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Admin.models import *

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def staff_team_bookings(request):
    staff_email = request.data.get('email_id_staff')

    if not staff_email:
        return Response({'status': 'error', 'message': 'Email is required'}, status=400)

    try:
        staff = StaffTBL.objects.get(email_id_staff=staff_email)
    except StaffTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Staff not found'}, status=404)

    # Get bookings assigned to the same team and same owner
    bookings = BookingTBL.objects.filter(
        assigned_team=staff.assigned_to,
        service__email_id_owner=staff.email_id_owner
    )

    booking_list = []
    for b in bookings:
        booking_list.append({
            'id': b.id,
            'items': b.service.items,
            'description': b.service.description,
            'rate': b.rate,
            'datetime': b.datetime.strftime('%Y-%m-%d %H:%M'),
            'approvalStatus': b.Approvalstatus,
            'paymentStatus': b.PaymentStatus,
            'workCompletedStatus': b.WorkCompletedSts,
            'customerName': b.email_id_customer.name,
        })

    return Response({
        'status': 'success',
        'team': staff.assigned_to,
        'bookings': booking_list
    })




@api_view(['POST'])
def mark_work_done(request):
    booking_id = request.data.get('booking_id')

    if not booking_id:
        return Response({'status': 'error', 'message': 'Booking ID is required'}, status=400)

    try:
        booking = BookingTBL.objects.get(id=booking_id)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=404)

    booking.WorkCompletedSts = 1
    booking.save()

    return Response({'status': 'success', 'message': 'Work marked as completed successfully'})


@api_view(['POST'])
def get_staff_for_booking(request):
    booking_id = request.data.get('booking_id')

    if not booking_id:
        return Response({'status': 'error', 'message': 'Booking ID is required'}, status=400)

    try:
        booking = BookingTBL.objects.get(id=booking_id)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=404)

    # Get team name and owner from the booking's service
    team_name = booking.assigned_team
    owner = booking.service.email_id_owner

    # Get all staff in the team, under same owner, excluding managers (staff_type != '1')
    staff_members = StaffTBL.objects.filter(
        assigned_to=team_name,
        email_id_owner=owner,
    ).exclude(staff_type='1')  # Exclude manager

    staff_list = []
    for staff in staff_members:
        staff_list.append({
            'name': staff.name,
            'email': staff.email_id_staff,
            'mob_no': staff.mob_no,
            'staff_type': staff.staff_type,
        })

    return Response({'status': 'success', 'team': team_name, 'staff': staff_list})



@api_view(['POST'])
def send_chat_message(request):
    booking_id = request.data.get('bookingid')
    message = request.data.get('message')
    sts = request.data.get('sts')  #1 = Manager to staff 2- staff to manager
    staff_type = request.data.get('staff_type')
    staff_email = request.data.get('staff_email')

    if not (booking_id and message and sts and staff_type):
        return Response({'status': 'error', 'message': 'All fields are required'}, status=400)

    try:
        booking = BookingTBL.objects.get(id=booking_id)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=404)

    chat = ManagerStaffChat.objects.create(
        bookingid=booking,
        message=message,
        sts=sts,
        staff_type=staff_type,
        staff_email=staff_email
    )

    return Response({'status': 'success', 'message': 'Message sent successfully'})


@api_view(['POST'])
def fetch_chat_messages(request):
    booking_id = request.data.get('bookingid')
    staff_email = request.data.get('staff_email')  # Ex: "2" for chef

    if not booking_id or not staff_email:
        return Response({'status': 'error', 'message': 'Booking ID and Staff email are required'}, status=400)

    try:
        booking = BookingTBL.objects.get(id=booking_id)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=404)

    chats = ManagerStaffChat.objects.filter(bookingid=booking, staff_email=staff_email).order_by('timestamp')

    chat_list = []
    for chat in chats:
        chat_list.append({
            'message': chat.message,
            'sts': chat.sts,  # 1 = Manager to Staff, 2 = Staff to Manager
            'staff_type': chat.staff_type,
            'staff_email':chat.staff_email,
            'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return Response({'status': 'success', 'chat': chat_list})

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def my_earnings(request):
    staff_email = request.data.get('email_id_staff')

    if not staff_email:
        return Response({'status': 'error', 'message': 'Email is required'}, status=400)

    try:
        staff = StaffTBL.objects.get(email_id_staff=staff_email)
    except StaffTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Staff not found'}, status=404)

    # Get completed bookings for this staff's team, with payment done
    completed_bookings = BookingTBL.objects.filter(
        assigned_team=staff.assigned_to,
        WorkCompletedSts=1,
        PaymentStatus=1,
        service__email_id_owner=staff.email_id_owner
    )

    total_works = completed_bookings.count()
    total_earnings = total_works * staff.wage

    booking_details = []
    for b in completed_bookings:
        booking_details.append({
            'booking_id': b.id,
            'item': b.items,
            'rate': staff.wage,
            'date': b.datetime.strftime('%Y-%m-%d %H:%M'),
        })

    return Response({
        'status': 'success',
        'staff_name': staff.name,
        'team': staff.assigned_to,
        'wage_per_work': staff.wage,
        'total_completed_works': total_works,
        'total_earnings': total_earnings,
        'details': booking_details
    })


