from django.shortcuts import render

from sales.models import Sale

from django.utils import timezone
from datetime import timedelta

def reports(request):

    sales = Sale.objects.select_related(
        "created_by",
        "shop"
    ).prefetch_related(
        "items"
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