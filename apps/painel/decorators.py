from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def admin_required(view_func):

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_staff:
            messages.error(
                request,
                "Você não possui permissão para acessar esta página."
            )
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper