from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = (
        "price",
        "quantity",
        "unit_price",
        "total_price",
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "customer_name",
        "grand_total",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "invoice_number",
        "customer_name",
        "customer_phone",
    )

    list_filter = (
        "payment_method",
        "created_at",
    )

    inlines = [SaleItemInline]


admin.site.register(SaleItem)