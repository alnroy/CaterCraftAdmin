from rest_framework import serializers
from .models import *

class FeedbackAdminViewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    ownername = serializers.SerializerMethodField()
    feedback = serializers.CharField()

    class Meta:
        model = FeedbackTBL
        fields = ['username', 'service', 'ownername', 'feedback']

    def get_username(self, obj):
        return obj.email_id_customer.name

    def get_service(self, obj):
        return obj.bookingid.service.items if obj.bookingid and obj.bookingid.service else ""

    def get_ownername(self, obj):
        return obj.bookingid.service.email_id_owner.name if obj.bookingid and obj.bookingid.service and obj.bookingid.service.email_id_owner else ""





class BookingViewSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_email = serializers.SerializerMethodField()
    customer_mobile = serializers.SerializerMethodField()
    service_item = serializers.SerializerMethodField()
    service_rate = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = BookingTBL
        fields = [
            'datetime', 'service_item', 'service_rate',
            'customer_name', 'customer_email', 'customer_mobile',
            'owner_name', 'company_name'
        ]

    def get_customer_name(self, obj):
        return obj.email_id_customer.name

    def get_customer_email(self, obj):
        return obj.email_id_customer.email_id_customer

    def get_customer_mobile(self, obj):
        return obj.email_id_customer.mob_no

    def get_service_item(self, obj):
        return obj.service.items if obj.service else ""

    def get_service_rate(self, obj):
        return obj.service.rate if obj.service else 0.0

    def get_owner_name(self, obj):
        return obj.service.email_id_owner.name if obj.service and obj.service.email_id_owner else ""

    def get_company_name(self, obj):
        return obj.service.email_id_owner.company_name if obj.service and obj.service.email_id_owner else ""



class OwnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerRegTBL
        fields = [
            'name', 'address', 'mob_no', 'email_id_owner',
            'status', 'company_name', 'license_document'
        ]



from rest_framework import serializers

class CustomerRegTBLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRegTBL
        fields = '__all__'  # or you can specify the fields you want to expose


