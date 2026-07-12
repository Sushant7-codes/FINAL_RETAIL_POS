from decimal import Decimal
from django.db import transaction

from .models import Sale, SaleItem
from shop.models import Price


@transaction.atomic
def create_sale(
    *,
    user,
    customer_name,
    customer_phone,
    discount_percent,
    payment_method,
    cash_received,
    change_amount,
    cart,
):

    subtotal = Decimal("0")
    cart_items = []

    for entry in cart:

        product = Price.objects.select_related("item").get(
            id=entry["price_id"]
        )

        quantity = int(entry["quantity"])

        if quantity > product.stock:
            raise Exception(
                f"{product.name} has insufficient stock."
            )

        total = product.amount * quantity

        subtotal += total

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "unit_price": product.amount,
            "total": total,
        })

    discount_amount = (
        subtotal * Decimal(str(discount_percent))
    ) / Decimal("100")

    grand_total = subtotal - discount_amount

    sale = Sale.objects.create(

        shop=user.shop,
        customer_name=customer_name,
        customer_phone=customer_phone,

        subtotal=subtotal,
        discount_percent=discount_percent,
        discount_amount=discount_amount,
        grand_total=grand_total,

        payment_method=payment_method,
        cash_received=cash_received,
        change_amount=change_amount,

        created_by=user,
    )

    for item in cart_items:

        SaleItem.objects.create(

            sale=sale,
            price=item["product"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            total_price=item["total"],
        )

        product = item["product"]
        product.stock -= item["quantity"]
        product.save()

    return sale