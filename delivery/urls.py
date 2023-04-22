from delivery import views
from django.urls import path, re_path

urlpatterns = [
    re_path("signup/", views.signup, name = "signup"),
    re_path("reset/", views.reset_password, name = "reset_password"),
    re_path("get_deliveries/", views.get_deliveries, name = "get_deliveries"),
    re_path("get_location/", views.get_location, name = "get_location")
]
