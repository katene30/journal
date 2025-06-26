from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='entries/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # Optional URL for including your own vanilla Django urls/views
    # re_path(r'', include('myapp.urls')),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r'', include(wagtail_urls)),
]
