from django.shortcuts import render, redirect
from .forms import RetailAdminRegisterForm, RetailAdminLoginForm

def retail_admin_register(request):
    if request.method == "POST":
        form = RetailAdminRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:retail_admin_login")

        context = {"form": form}
        return render(request, "accounts/register.html", context)

    form = RetailAdminRegisterForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def retail_admin_login(request):
    form = RetailAdminLoginForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)