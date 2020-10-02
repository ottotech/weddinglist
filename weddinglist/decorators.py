# Python imports
from functools import wraps

# Django imports
from django.shortcuts import redirect


def redirect_if_guest(view_func):
    @wraps(view_func)
    def _wrapped_view(req, *args, **kwargs):
        if hasattr(req.user, "guest") and not req.is_ajax():
            return redirect("/guest-view")
        return view_func(req, *args, **kwargs)
    return _wrapped_view

