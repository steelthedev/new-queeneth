from django.http import HttpResponseForbidden
from .models import Staff

def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        is_staff = Staff.objects.filter(user = request.user).exists()
        if request.user.is_authenticated and is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Permission Denied")

    return _wrapped_view
