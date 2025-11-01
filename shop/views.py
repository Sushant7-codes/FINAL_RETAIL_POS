from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from shop.models import Item,Price
from django.urls import reverse
from urllib.parse import urlencode
import random

from accounts.models import CustomUser
from shop.forms import(
    ShopForm,
    ItemForm,
    PriceForm,
    StaffRegistrationForm,
)
# from shop.models import Fee, Grade, TempCSVFile
# from shop.background_tasks import bulk_create_students_from_csv
from shop.filters import StaffFilter


from django.core.paginator import Paginator


@require_http_methods(["GET", "POST"])
@login_required
def shop_register(request):
    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES, request=request)  # ✅ pass request here
        if form.is_valid():
            form.save()  # ✅ no request here
            messages.success(request, "Shop registered successfully!")
            return redirect("shop:shop_profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ShopForm(request=request)

    return render(request, "shop/register.html", {"form": form})


@login_required
def shop_profile(request):
    shop_admin = request.user
    try:
        shop_data = shop_admin.shop
    except Exception:
        messages.warning(request, "You need to register your shop first.")
        return redirect("shop:shop_register")

    context = {
        'admin': shop_admin,
        'shop': shop_data
    }
    return render(request, "shop/profile.html", context)


@login_required
def shop_update(request):
    shop_instance = request.user.shop
    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES, instance=shop_instance, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "Shop updated successfully!")
            return redirect("shop:shop_profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ShopForm(instance=shop_instance, request=request)

    from_submission_url = reverse_lazy("shop:shop_update")
    context = {
        "form": form,
        "form_submission_url": from_submission_url
    }
    return render(request, "shop/update-shop-info.html", context)


def item_list(request):
    form=ItemForm(request.POST,request=request)
    if form.is_valid():
        
        try:
            saved_item=form.save()
        except IntegrityError:
            return JsonResponse(
                {"success":False,"message":"Item already exists !"}
            )

        else:
            saved_item_dict={
                "id":saved_item.id,
                "name":saved_item.name,
                "barcode": saved_item.barcode,  # Add barcode to response
            }
            return JsonResponse(
                {"success":True,
                 "message":"Item added successfully !",
                 "data":saved_item_dict,
                 }
            )

    
    form=ItemForm()
    item_list=request.user.shop.items.all()
    
    context={"form":form,"item_list":item_list}
    return render(request, "shop/item-create-form.html", context)

def item_list_delete(request,pk):
    
    try:
        Item.objects.get(id=pk).delete()
    
    except Item.DoesNotExist:
        return JsonResponse(
            {"success":False,"message":"Item does not exist !"}
        )
    else:
        return JsonResponse(
            {"success":True,"message":"Item deleted successfully !"}
        )
        
def item_update(request,pk):
    
    try:
        item=Item.objects.get(id=pk)
    except Item.DoesNotExist:
        messages.error(request, "Item does not exist")
        return redirect("shop:item_list")
    
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item, request=request)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully!")
            return redirect("shop:item_list")
        
        messages.error(request, "Please correct the errors below.")
        return redirect("shop:item_list")
        
    else:
        form=ItemForm(instance=item, request=request)
        context={"form":form,"item":item}
        return render(request, "shop/item-update-form.html", context)
    
def price(request):
    
    if request.method == "POST":
        item_id=request.POST.get("item_id")
        try:
            item=Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse({"success":False,"message":"Item does not exist !"})
        
        form = PriceForm(request.POST)
        if form.is_valid():
            try:
                saved_price=form.save(item=item)
            except IntegrityError:
                return JsonResponse(
                    {"success":False,"message":"Price already exists !"}
                )
                
            response={
                "success":True,
                "message":"Price added successfully !",
                "data":{
                    "id":saved_price.id,
                    "name":saved_price.name,
                    "amount":saved_price.amount,
                    "stock":saved_price.stock,
                    "barcode": saved_price.barcode,  # Add barcode to response
                },
            }
            return JsonResponse(response)
    
    
    item_id=request.GET.get("item_id")
    try:
        item=Item.objects.get(id=item_id)
        prices=item.prices.all()
    except Item.DoesNotExist:
        messages.error(request, "Item does not exist")
        return redirect("shop:item_list")
    
    form=PriceForm()
    context={"form":form,"item":item,"prices":prices}
    
    
    return render(request, "shop/price-create.html",context)


def price_delete(request,pk):
    
    try:
        Price.objects.get(id=pk).delete()
    
    except Price.DoesNotExist:
        return JsonResponse(
            {"success":False,"message":"Price does not exist !"}
        )
    else:
        return JsonResponse(
            {"success":True,"message":"Price deleted successfully !"}
        )


def price_update(request,pk):
    
    try:
        price=Price.objects.get(id=pk)
        base_url=reverse("shop:price")
        query_string=urlencode({"item_id":price.item.id})
        url=f"{base_url}?{query_string}"
    except Price.DoesNotExist:
        messages.error(request, "Price does not exist")
        return redirect(url)
    
    if request.method == "POST":
        form = PriceForm(request.POST, instance=price)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Price updated successfully!")
            return redirect(url)
        
        messages.error(request, "Please correct the errors below.")
        return redirect(url)
        
    else:
        form=PriceForm(instance=price)
        context={"form":form,}
        return render(request, "shop/price-update.html", context)


def staffs(request):
    # --- Handle Staff Registration ---
    if request.method == "POST":
        form = StaffRegistrationForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            staff = form.save(commit=False)

            # --- Generate unique username automatically ---
            first = staff.first_name[:3].lower() if staff.first_name else "usr"
            last = staff.last_name[-3:].lower() if staff.last_name else str(random.randint(100, 999))
            base_username = f"{first}{last}"

            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            staff.username = username
            staff.is_staff = True
            staff.save()

            messages.success(request, f"Staff registered successfully! Username: {staff.username}")
            return redirect(request.path)
    else:
        form = StaffRegistrationForm(request=request)

    # --- Staff List with Filtering and Pagination ---
    all_staffs = CustomUser.objects.filter(role=CustomUser.Roles.STAFF).order_by("-id")
    
    # Apply filters
    filtered_staffs = StaffFilter(request.GET, queryset=all_staffs)
    
    # Paginate the filtered results
    paginator = Paginator(filtered_staffs.qs, 8)  # Use filtered_staffs.qs
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "staffs": page_obj,
        "page_obj": page_obj,
        "filter_form": filtered_staffs.form,  # Pass the filter form
        "filtered_staffs": filtered_staffs,
    }

    return render(request, "shop/staffs.html", context)