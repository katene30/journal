from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path

from .views import spa_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='entries/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # API
    path('api/', include('entries.api_urls')),

    # SvelteKit SPA (new frontend)
    re_path(r'^app(?:/.*)?$', spa_view, name='spa'),

    # Django templates (existing)
    path('', include('entries.urls')),
]
