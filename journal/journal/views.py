from django.http import HttpResponse
from django.conf import settings
from django.middleware.csrf import get_token
import os

from dj_rest_auth.views import PasswordResetView
from rest_framework.throttling import ScopedRateThrottle


def spa_view(request):
    """Serve the SvelteKit SPA for any non-API route.

    Deliberately public: the SPA shell holds no user data, its own layout
    redirects logged-out users to /app/login, and the API enforces auth.
    """
    # Ensure CSRF cookie is set
    get_token(request)

    index_path = os.path.join(settings.STATIC_ROOT, 'frontend', 'index.html')

    try:
        with open(index_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    except FileNotFoundError:
        return HttpResponse(
            "Frontend not built. Run 'npm run build' in the frontend directory.",
            status=503
        )


class ThrottledPasswordResetView(PasswordResetView):
    """Password reset request, rate-limited per IP (see DEFAULT_THROTTLE_RATES)."""
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'password_reset'
