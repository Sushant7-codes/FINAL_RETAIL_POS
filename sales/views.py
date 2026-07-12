import json

from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils import timezone
from django.shortcuts import redirect

from .models import Sale, SaleItem
from shop.models import Price

from .services import initiate_khalti_payment
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404, render

from .utils import create_sale

@require_POST
@transaction.atomic
def checkout(request):

    try:

        data = json.loads(request.body)

        sale = create_sale(

            user=request.user,
            customer_name=data["customer_name"],
            customer_phone=data["customer_phone"],
            discount_percent=Decimal(
                str(data["discount_percent"])
            ),
            payment_method=data.get(
                "payment_method",
                "cash"
            ),
            cash_received=Decimal(
                str(data.get("cash_received", 0))
            ),
            change_amount=Decimal(
                str(data.get("change_amount", 0))
            ),
            cart=data["cart"],
        )
        return JsonResponse({

            "success": True,
            
            "sale_id": sale.id,
            "invoice": sale.invoice_number,
            "grand_total": str(sale.grand_total),
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)

@require_POST
def khalti_initiate(request):

    data = json.loads(request.body)
    
    request.session["khalti_checkout"] = data
    request.session.modified = True

    subtotal = Decimal("0")

    for entry in data["cart"]:

        product = Price.objects.get(id=entry["price_id"])

        subtotal += product.amount * entry["quantity"]

    discount = (
        subtotal * Decimal(str(data["discount_percent"]))
    ) / Decimal("100")

    grand_total = subtotal - discount

    payload = {

        "return_url": "http://127.0.0.1:8000/sales/khalti/success/",

        "website_url": "http://127.0.0.1:8000",

        "amount": int(grand_total * 100),

        "purchase_order_id": "TEST123",

        "purchase_order_name": "Retail POS Sale",

        "customer_info": {

            "name": data["customer_name"],

            "phone": data["customer_phone"]

        }

    }
    
    response = initiate_khalti_payment(payload)

    print(response.status_code)
    print(response.text)

    return JsonResponse(response.json(), status=response.status_code)


def khalti_success(request):

    status = request.GET.get("status")

    if status != "Completed":
        request.session.pop("khalti_checkout", None)
        return redirect("/billing/billing/")

    data = request.session.get("khalti_checkout")

    if not data:
        return HttpResponse("Session expired.")

    try:

        sale = create_sale(

            user=request.user,
            customer_name=data["customer_name"],
            customer_phone=data["customer_phone"],
            discount_percent=Decimal(
                str(data["discount_percent"])
            ),

            payment_method="khalti",
            cash_received=Decimal("0"),
            change_amount=Decimal("0"),
            cart=data["cart"]

        )

        request.session.pop("khalti_checkout", None)

        return redirect(
            "sale_success",
            invoice_number=sale.invoice_number
        )

    except Exception as e:

        request.session.pop("khalti_checkout", None)

        return HttpResponse(str(e))
    
    
def invoice_view(request, invoice_number):

    sale = get_object_or_404(
        Sale.objects.select_related(
            "shop",
            "created_by"
        ).prefetch_related(
            "items__price"
        ),
        invoice_number=invoice_number
    )

    return render(
        request,
        "sales/invoice.html",
        {
            "sale": sale
        }
    )
    
def sale_success(request, invoice_number):

    sale = get_object_or_404(
        Sale,
        invoice_number=invoice_number
    )
    return render(
        request,
        "sales/sale_success.html",
        {
            "sale": sale
        }
    )