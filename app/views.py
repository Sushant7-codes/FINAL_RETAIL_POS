from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.forms import ShopForm
from django.urls import reverse_lazy
from accounts.models import CustomUser
from shop.models import Shop, Price
from sales.models import Sale, SaleItem
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal

from django.db.models.functions import TruncDate
from django.db.models import Sum
import json

@login_required
def dashboard(request):

    has_shop = False
    context = {}

    # Staff users always have access to the dashboard
    if request.user.role == CustomUser.Roles.STAFF:
        has_shop = True

    # Shop Admin
    else:
        shop = Shop.objects.filter(admin_user=request.user).first()

        if shop:
            has_shop = True
        else:
            messages.info(
                request,
                "Welcome to the dashboard, please create a shop to get started!"
            )

            context["form"] = ShopForm()
            context["form_submission_url"] = reverse_lazy("shop:shop_register")

    context["has_shop"] = has_shop
    
    if has_shop:

        if request.user.role == CustomUser.Roles.SHOP_ADMIN:
            shop = request.user.shop
        else:
            shop = request.user.workplace
    
        today = timezone.localdate()
    
        total_revenue = (
            Sale.objects.filter(shop=shop)
            .aggregate(total=Sum("grand_total"))["total"]
            or 0
        )

        today_revenue = (
            Sale.objects.filter(
                shop=shop,
                created_at__date=today
            ).aggregate(total=Sum("grand_total"))["total"]
            or 0
        )
        
        from datetime import timedelta
        
        last_7_days = []
        
        for i in range(6, -1, -1):
        
            day = today - timedelta(days=i)
        
            revenue = (
                Sale.objects.filter(
                    shop=shop,
                    created_at__date=day
                ).aggregate(
                    total=Sum("grand_total")
                )["total"] or 0
            )
        
            last_7_days.append({
            
                "day": day.strftime("%a"),
                "revenue": float(revenue)
        
            })
        
        context["daily_sales_chart"] = json.dumps(last_7_days)
        
        DAILY_GOAL = Decimal("75000")
        goal_percent = min(
            round((today_revenue / DAILY_GOAL) * 100, 1)
            if DAILY_GOAL else 0,
            100
        )
        remaining_goal = max(
            DAILY_GOAL - today_revenue,
            0
        )
        
        total_sales = Sale.objects.filter(shop=shop).count()
        low_stock = Price.objects.filter(
            item__shop=shop,
            stock__lte=5
        ).count()
        total_products = Price.objects.filter(
            item__shop=shop
        ).count()
        
        top_sales_today = (
            Sale.objects.filter(
                shop=shop,
                created_at__date=today
            )
            .order_by("-grand_total")[:3]
        )

        context["top_sales_today"] = top_sales_today
        
        top_products = (

            SaleItem.objects
            .filter(
                sale__shop=shop
            )
            .values(
                "price__name"
            )
            .annotate(
                total_sold=Sum("quantity")
            )
            .order_by("-total_sold")[:5]
        )
        context["top_products"] = top_products

        recent_transactions = (

            Sale.objects.filter(
                shop=shop
            )
            .select_related("created_by")
            .order_by("-created_at")[:5]
        
        )
        
        context["recent_transactions"] = recent_transactions

        context.update({
            "today_revenue": today_revenue,
            "total_revenue": total_revenue,
            "total_sales": total_sales,
            "low_stock": low_stock,
            "total_products": total_products,
            "daily_goal": DAILY_GOAL,
            "goal_percent": goal_percent,
            "remaining_goal": remaining_goal,
        })
    
    return render(request, "app/dashboard.html", context)