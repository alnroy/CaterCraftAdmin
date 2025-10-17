from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Admin.models import *

@api_view(['POST'])
def view_customer_profile(request):
    email = request.data.get('email')

    if not email:
        return Response({'status': 'error', 'message': 'email is required'}, status=400)

    try:
        customer = CustomerRegTBL.objects.get(email_id_customer=email)
    except CustomerRegTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Customer not found'}, status=404)

    data = {
        'name': customer.name,
        'address': customer.address,
        'mob_no': customer.mob_no,
        'id_proof': customer.id_proof,
        'status': customer.status,
    }

    return Response({'status': 'success', 'profile': data}, status=200)

@api_view(['POST'])
def update_customer_profile(request):
    email = request.data.get('email')

    if not email:
        return Response({'status': 'error', 'message': 'email is required'}, status=400)

    try:
        customer = CustomerRegTBL.objects.get(email_id_customer=email)
    except CustomerRegTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Customer not found'}, status=404)

    customer.name = request.data.get('name', customer.name)
    customer.address = request.data.get('address', customer.address)
    customer.mob_no = request.data.get('mob_no', customer.mob_no)
    customer.id_proof = request.data.get('id_proof', customer.id_proof)
    customer.save()

    return Response({'status': 'success', 'message': 'Profile updated successfully'}, status=200)



@api_view(['GET'])
def view_all_services(request):
    services = ServiceTBL.objects.filter(status=1)  # only active services
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



from django.utils import timezone

@api_view(['POST'])
def book_service(request):
    service_id = request.data.get('service_id')
    email_id_customer = request.data.get('email_id_customer')
    datetime_str = request.data.get('datetime')

    if not service_id or not email_id_customer or not datetime_str:
        return Response({'status': 'error', 'message': 'Missing required fields'}, status=400)

    try:
        service = ServiceTBL.objects.get(service_id=service_id)
        customer = CustomerRegTBL.objects.get(email_id_customer=email_id_customer)
    except ServiceTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Service not found'}, status=404)
    except CustomerRegTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Customer not found'}, status=404)

    booking = BookingTBL.objects.create(
        service=service,
        datetime=datetime_str,
        items=service.description,  # Use description as items
        rate=service.rate,          # Use rate from service
        email_id_customer=customer
    )

    return Response({
        'status': 'success',
        'message': 'Booking created successfully',
        'booking_id': booking.id
    }, status=201)




@api_view(['POST'])
def view_my_bookings(request):
    email = request.data.get('email_id_customer')

    if not email:
        return Response({'status': 'error', 'message': 'email_id_customer is required'}, status=400)

    bookings = BookingTBL.objects.filter(email_id_customer__email_id_customer=email).order_by('-id')

    booking_list = []
    for booking in bookings:
        booking_list.append({
            'id': booking.id,
            'service': booking.service.items,
            'rate': booking.rate,
            'description': booking.service.description,
            'datetime': booking.datetime.strftime('%Y-%m-%d %H:%M'),
            'approvalStatus': booking.Approvalstatus,
            'paymentStatus': booking.PaymentStatus,
            'workCompletedStatus': booking.WorkCompletedSts,
            'assignedTeam': booking.assigned_team,
            'ownerName': booking.service.email_id_owner.name,
            'ownerCompany': booking.service.email_id_owner.company_name,
        })

    return Response({'status': 'success', 'bookings': booking_list}, status=200)



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
    sts = 1

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
def make_payment(request):
    booking_id = request.data.get('booking_id')

    if not booking_id:
        return Response({'status': 'error', 'message': 'booking_id is required'}, status=400)

    try:
        booking = BookingTBL.objects.get(id=booking_id)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=404)

    if booking.PaymentStatus == 1:
        return Response({'status': 'warning', 'message': 'Payment already done'}, status=200)

    booking.PaymentStatus = 1
    booking.save()

    return Response({'status': 'success', 'message': 'Payment marked as done'}, status=200)



from django.utils import timezone

@api_view(['POST'])
def give_feedback(request):
    email = request.data.get('email_id_customer')
    booking_id = request.data.get('bookingid')
    feedback_text = request.data.get('feedback')

    if not email or not booking_id or not feedback_text:
        return Response({'status': 'error', 'message': 'Missing required fields'}, status=400)

    try:
        customer = CustomerRegTBL.objects.get(email_id_customer=email)
    except CustomerRegTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Customer not found'}, status=404)

    try:
        booking = BookingTBL.objects.get(id=booking_id, email_id_customer=customer)
    except BookingTBL.DoesNotExist:
        return Response({'status': 'error', 'message': 'Booking not found'}, status=404)

    FeedbackTBL.objects.create(
        email_id_customer=customer,
        bookingid=booking,
        feedback=feedback_text,
        datetime=timezone.now()
    )

    return Response({'status': 'success', 'message': 'Feedback submitted'}, status=200)
