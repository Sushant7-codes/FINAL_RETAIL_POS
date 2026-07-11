from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("app.urls")),
    path("shop/", include(("shop.urls", "shop"), namespace="shop")),
    path("billing/", include("billing.urls")),
    path("sales/", include("sales.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
