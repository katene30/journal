from django.http import HttpResponse
from django.conf import settings
import os


def spa_view(request):
    """Serve the SvelteKit SPA for any non-API route."""
    index_path = os.path.join(settings.STATIC_ROOT, 'frontend', 'index.html')

    try:
        with open(index_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    except FileNotFoundError:
        return HttpResponse(
            "Frontend not built. Run 'npm run build' in the frontend directory.",
            status=503
        )
