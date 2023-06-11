from functools import wraps

from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()


def author_or_superuser_required(func):
    """Decorator that checks if the user is an owner of the page
    or superuser.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        username = kwargs.get("username")
        if not (request.user.is_superuser
                or request.user.username == username):
            return redirect("about:index")
        return func(request, *args, **kwargs)
    return wrapper
