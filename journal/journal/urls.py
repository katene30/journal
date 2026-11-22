from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from django.conf import settings
import mimetypes
import os

from .views import spa_view

mimetypes.add_type('application/manifest+json', '.webmanifest')


def serve_spa_static(request, path):
    """Serve SvelteKit static files from the frontend build."""
    document_root = os.path.join(settings.STATIC_ROOT, 'frontend')
    return serve(request, path, document_root=document_root)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth API (for SPA)
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # API
    path('api/', include('entries.api_urls')),

    # SvelteKit SPA static files
    re_path(r'^app/(?P<path>_app/.*)$', serve_spa_static),
    re_path(r'^app/(?P<path>robots\.txt|favicon\.ico|favicon-32x32\.png|icon\.svg|manifest\.webmanifest)$', serve_spa_static),
    re_path(r'^(?P<path>favicon\.ico)$', serve_spa_static),

    # SvelteKit SPA (new frontend)
    re_path(r'^app(?:/.*)?$', spa_view, name='spa'),

    # Everything lives in the SPA now
    path('', RedirectView.as_view(url='/app/', permanent=False)),
]
