from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "update-goal/",
        views.update_daily_goal,
        name="update_daily_goal",
    ),
]