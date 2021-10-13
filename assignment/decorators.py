from django.http import HttpResponseRedirect
from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

class SuperRequiredMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect("landing-page")
        return super().dispatch(request, *args, **kwargs)


class HODRequiredMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_hod:
            return redirect("landing-page")
        return super().dispatch(request, *args, **kwargs)


# user_login_required = user_passes_test(
#     lambda user: user.is_hod)

# def hod_user_required(view_func):
#     decorated_view_func = login_required(user_login_required(view_func))
#     return decorated_view_func


def hod_required(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/login/")
    else:
        if not request.user.is_hod:
            return redirect('landing-page')
        else:
            # return HttpResponseRedirect('/')
            return function(request, *args, **kwargs)
  return wrap
