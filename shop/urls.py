from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("register/", views.shop_register, name="shop_register"),
]