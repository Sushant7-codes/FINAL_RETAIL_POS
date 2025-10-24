from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("register/", views.shop_register, name="shop_register"),
    path("profile/", views.shop_profile, name="shop_profile"),
    path("update/", views.shop_update, name="shop_update"),
    path("item_list/", views.item_list, name="item_list"),
]