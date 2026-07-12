from django.urls import path
from . import views

urlpatterns = [

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),
    path(
        "khalti/initiate/",
        views.khalti_initiate,
        name="khalti_initiate"
    ),
]