from django.db import models
from accounts.models import CustomUser
from shop.models import Shop, Price


class Sale(models.Model):

    PAYMENT_CHOICES = [
        ("cash", "Cash"),
        ("esewa", "eSewa"),
        ("khalti", "Khalti"),
        ("card", "Card"),
    ]

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="sales"
    )

    customer_name = models.CharField(
        max_length=150
    )

    customer_phone = models.CharField(
        max_length=20
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    grand_total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )


    cash_received = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    change_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.invoice_number


class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items"
    )

    price = models.ForeignKey(
        Price,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.sale.invoice_number} - {self.price.name}"