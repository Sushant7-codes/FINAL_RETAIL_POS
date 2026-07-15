from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [

    path(
        "",
        views.reports,
        name="reports"
    ),
    path(
        "analytics/",
        views.sales_analytics,
        name="sales_analytics"
    ),
]