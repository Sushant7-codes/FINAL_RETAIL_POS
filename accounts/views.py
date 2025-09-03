from django.shortcuts import render, redirect
from .forms import RetailAdminRegisterForm, RetailAdminLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def retail_admin_register(request):
    if request.method == "POST":
        form = RetailAdminRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("accounts:retail_admin_login")

        context = {"form": form}
        return render(request, "accounts/register.html", context)

    form = RetailAdminRegisterForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def retail_admin_login(request):
    
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("app:dashboard")
            
        messages.error(request, "Invalid username or password")    
        return redirect("accounts:retail_admin_login")
        
    form = RetailAdminLoginForm()
    
    context = {"form": form}
    return render(request, "accounts/login.html", context)

def logout_view(request):
    logout(request)
    return redirect("accounts:retail_admin_login")

