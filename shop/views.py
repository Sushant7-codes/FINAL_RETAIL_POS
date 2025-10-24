from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse

from shop.forms import ShopForm,ItemForm


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
        form.save()

    return JsonResponse(
        {"success":True,"message":"Item added successfully!"}
        )
    
    form=ItemForm()
    return render(request, "shop/item-form.html",{"form":form})