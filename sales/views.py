import json

from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils import timezone

from .models import Sale, SaleItem
from shop.models import Price


@require_POST
@transaction.atomic
def checkout(request):

    try:

        data = json.loads(request.body)

        customer_name = data["customer_name"]
        customer_phone = data["customer_phone"]
        discount_percent = Decimal(str(data["discount_percent"]))
        cart = data["cart"]

        if not cart:

            return JsonResponse({       
                "success": False,       
                "message": "Cart is empty."     
            })
    
        subtotal = Decimal("0")
        
        cart_items = []

        for entry in cart:
        
            product = Price.objects.select_related("item").get(
                id=entry["price_id"]
            )
            quantity = int(entry["quantity"])

            if quantity > product.stock:
                return JsonResponse({
                    "success": False,
                    "message": f"{product.name} has insufficient stock."
                })

            total = product.amount * quantity

            subtotal += total
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "unit_price": product.amount,
                "total": total
            })
        
        discount_amount = (
            subtotal * discount_percent
        ) / Decimal("100")

        grand_total = subtotal - discount_amount

        # Validate everything here
        invoice = f"INV-{timezone.localtime().strftime('%Y%m%d%H%M%S')}"
        
        # Create Sale
        sale = Sale.objects.create(         
            shop=product.item.shop,         
            created_by=request.user,          
            customer_name=customer_name,            
            customer_phone=customer_phone,          
            subtotal=subtotal,          
            discount_percent=discount_percent,          
            discount_amount=discount_amount,            
            grand_total=grand_total,  
            invoice_number=invoice,  
            payment_method="cash",
        )

        # Create SaleItems
        for item in cart_items:

            SaleItem.objects.create(
                sale=sale,
                price=item["product"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                total_price=item["total"]
            )
    
            # Reduce Stock
            item["product"].stock -= item["quantity"]
            item["product"].save()

        return JsonResponse({    
            "success": True,
            "sale_id": sale.id,
            "invoice": sale.invoice_number,
            "grand_total": str(grand_total),
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)