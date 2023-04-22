from rest_framework import serializers
from delivery.models import users, orders, deliveries

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ('username', 'fullname', 'email', 'password', 'security_question_1', 'answer_1', 'security_question_2', 
        'answer_2', 'user_type')

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = ('trackingid', 'username', 'orderdate', 'destination_address', 'source_address', 'delivery_service', 
        'package_weight')

class DeliveriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = deliveries
        fields = ('trackingid', 'driver', 'status', 'current_city', 'current_state', 'latitude', 'longitude')