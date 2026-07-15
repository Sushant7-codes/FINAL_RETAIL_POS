from django.shortcuts import render
from sales.models import Sale, SaleItem
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Avg
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required

@login_required
def reports(request):
    if request.user.role == CustomUser.Roles.SHOP_ADMIN:
        shop = request.user.shop
    else:
        shop = request.user.workplace

    sales = (
        Sale.objects
        .filter(shop=shop)
        .select_related(
            "created_by",
            "shop"
        )
        .prefetch_related("items")
    )

    filter_by = request.GET.get("filter", "all")
    today = timezone.localdate()
    
    if filter_by == "today":
    
        sales = sales.filter(
            created_at__date=today
        )
    
    elif filter_by == "week":
    
        start = today - timedelta(days=today.weekday())
    
        sales = sales.filter(
            created_at__date__gte=start
        )
    
    elif filter_by == "month":
    
        sales = sales.filter(
            created_at__year=today.year,
            created_at__month=today.month
        )
        
    search = request.GET.get("search", "").strip()
    search_by = request.GET.get(
        "search_by",
        "invoice"
    )
    
    if search:
        if search_by == "invoice":      
            sales = sales.filter(
                invoice_number__icontains=search
            )       
        elif search_by == "phone":      
            sales = sales.filter(
                customer_phone__icontains=search
            )       
        elif search_by == "customer":       
            sales = sales.filter(
                customer_name__icontains=search
            )       
        elif search_by == "cashier":        
            sales = sales.filter(
                created_by__username__icontains=search
            )       
        elif search_by == "date":       
            sales = sales.filter(
                created_at__date=search
            )

    sales = sales.order_by("-created_at")
    
    context = {

        "sales": sales,
        "filter": filter_by,
        "search": search,
        "search_by": search_by,

    }

    return render(
        request,
        "reports/reports.html",
        context
    )
    
@login_required
def sales_analytics(request):   
    if request.user.role == CustomUser.Roles.SHOP_ADMIN:
        shop = request.user.shop
    else:
        shop = request.user.workplace

    sales = (
        Sale.objects
        .filter(shop=shop)
        .select_related(
            "created_by",
            "shop"
        )
    ) 
    
    start = request.GET.get("start")
    end = request.GET.get("end")    
    if start and end:   
        sales = sales.filter(
            created_at__date__range=[start, end]
        )   
    revenue = (
        sales.aggregate(
            total=Sum("grand_total")
        )["total"]
        or 0
    )   
    total_sales = sales.count() 
    average_sale = (
        sales.aggregate(
            avg=Avg("grand_total")
        )["avg"]
        or 0
    )   
    total_discount = (
        sales.aggregate(
            total=Sum("discount_amount")
        )["total"]
        or 0
    )   
    top_products = (    
        SaleItem.objects.filter(
            sale__in=sales
        )
        .values("price__name")
        .annotate(
            total_sold=Sum("quantity")
        )
        .order_by("-total_sold")[:5]    
    )   
    biggest_sale = sales.order_by(
        "-grand_total"
    ).first()   
    payment_split = {}  
    for payment in ["cash", "khalti"]:  
        payment_split[payment] = (  
            sales.filter(
                payment_method=payment
            ).aggregate(
                total=Sum("grand_total")
            )["total"]  
            or 0    
        )   
    recent_transactions = sales.order_by(
        "-created_at"
    )[:10]  
    return render(  
        request,    
        "reports/sales_analytics.html", 
        {   
            "revenue": revenue, 
            "total_sales": total_sales, 
            "average_sale": average_sale,   
            "total_discount": total_discount,   
            "top_products": top_products,   
            "biggest_sale": biggest_sale,   
            "payment_split": payment_split, 
            "recent_transactions": recent_transactions, 
            "start": start, 
            "end": end, 
        }
    )