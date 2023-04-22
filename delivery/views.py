from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http.response import JsonResponse
from django.db import connection
from django.core.mail import send_mail
import random
import string

from delivery.models import users, orders, deliveries
from delivery.serializers import UsersSerializer, DeliveriesSerializer, OrdersSerializer

# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        json_parser = JSONParser()
        signup_data = json_parser.parse(request)
        users_serializer = UsersSerializer(data=signup_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse(users_serializer.errors, safe=False)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        json_parser = JSONParser()
        login_data = json_parser.parse(request)


# Helper View to generate a random password
def generate_password(length):
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    return password

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        json_parser = JSONParser()
        reset_data = json_parser.parse(request)
        email = reset_data.get('email')

        # Check if the user exists in database
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM delivery_users WHERE email = %s', (email,))
        results = cursor.fetchall()

        if results is None:
            return JsonResponse('Error: User Not Found')
        
        # Generate a random password and update the user's password in the database
        password = generate_password(10)
        cursor.execute('UPDATE delivery_users SET password = %s WHERE email = %s', (password, email))
        connection.commit()

        subject = 'Password Reset Request'
        message = "To reset your password, please use the one time password: "+password+"\n\nIf you did not request a password reset, please ignore this email."
        from_email = 'sreekavya.shetty@gmail.com'
        recipient_list = [email]     # ['singh.shubhams1397@gmail.com']
        html_message = "<p>To reset your password, please use the one time password:</p><p>"+password+"</p><p>If you did not request a password reset, please ignore this email.</p>"
        sent = send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        if sent:
            return JsonResponse("Mail Sent Successfully", safe=False)
        else:
            return JsonResponse("Failed to Send Mail", safe=False)


@csrf_exempt
def get_deliveries(request):
    # Get all deliveries where status != Delivered
    delivery_data = deliveries.objects.exclude(status = 'Delivered')
    delivery_serializer = DeliveriesSerializer(delivery_data, many = True)
    # delivery_json = JSONRenderer().render(delivery_serializer.data)

    return JsonResponse(delivery_serializer.data, safe = False)

         
@csrf_exempt
def place_order(request):
    json_parser = JSONParser()
    order_data = json_parser.parse(request)
    order_serializer = OrdersSerializer(data=order_data)
    if order_serializer.is_valid():
        order_serializer.save()
        return JsonResponse("Order Placed Successfully", safe=False)
    return JsonResponse(order_serializer    .errors, safe=False)

@csrf_exempt
def get_location(request):
    json_parser = JSONParser()
    tracking_data = json_parser.parse(request)
    trackingId = tracking_data.get('trackingId')

    # Check if the user exists in database
    cursor = connection.cursor()
    cursor.execute('SELECT latitude as lat, longitude as lng FROM delivery_deliveries WHERE trackingid = %s', (trackingId,))
    results = cursor.fetchall()
    print(results)

    # Create a Dictionaryto capture latitude and longitude values
    location = {'lat': results[0][0], 'lng': results[0][1]} if results else None

    return JsonResponse(location, safe=False)
    






