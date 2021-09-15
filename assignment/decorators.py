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