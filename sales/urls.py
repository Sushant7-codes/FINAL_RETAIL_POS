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
    
    path(
    "khalti/success/",
    views.khalti_success,
    name="khalti_success",
    ),
    path(
        "invoice/<str:invoice_number>/",
        views.invoice_view,
        name="invoice"
    ),
    path(
        "success/<str:invoice_number>/",
        views.sale_success,
        name="sale_success"
    ),
]