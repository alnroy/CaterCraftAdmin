from rest_framework import serializers
from Admin.models import *


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRegTBL
        fields = '__all__'



class OwnerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerRegTBL
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    user_type = serializers.IntegerField()  # 1 = Owner, 2 = Staff, 3 = Customer
