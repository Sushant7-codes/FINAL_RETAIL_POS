from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.retail_admin_register, name="retail_admin_register"),
    path("login/", views.retail_admin_login, name="retail_admin_login"),
    path("logout/", views.logout_view, name="logout_view"),
]