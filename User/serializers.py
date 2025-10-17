# serializers.py

from rest_framework import serializers
from Admin.models import *

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTBL
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    customer_email = serializers.CharField(source='email_id_customer.email_id_customer')
    booking_id = serializers.IntegerField(source='bookingid.id')

    class Meta:
        model = FeedbackTBL
        fields = ['feedback_id', 'customer_email', 'booking_id', 'feedback', 'datetime']
