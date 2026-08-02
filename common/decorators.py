from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import CustomUser


def shop_required(view_func):
    """
    Decorator that ensures the logged-in user has a shop (or workplace for staff).
    If not, redirects to the dashboard which shows the shop registration form,
    with a clear message telling the user what they need to do first.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        if user.role == CustomUser.Roles.SHOP_ADMIN:
            has_shop = user.shop is not None
        else:
            # Staff — need a workplace assigned
            has_shop = user.workplace is not None

        if not has_shop:
            messages.warning(
                request,
                "You need to register your shop before you can access that page."
            )
            return redirect("app:dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper
