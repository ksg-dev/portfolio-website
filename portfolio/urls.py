"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Custom Admin
    path('aura-admin/', include('core.admin_urls', namespace='aura_admin')),
    # Core app URLs (homepage, about, contact)
    path("", include("core.urls")),
    # Projects app URLs
    path("systems/", include("projects.urls")),
    # Blog app URLs
    path("datalogs/", include("blog.urls", namespace="blog")),
    path("markdownx/", include("markdownx.urls")),
    # Test new AURA global filters/templatetags
    path("test-aura/", TemplateView.as_view(template_name="test_aura.html"), name="test_aura")
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers (Django will automatically use these)
handler404 = 'core.views.custom_404_view'
handler500 = 'core.views.custom_500_view'
handler403 = 'core.views.custom_403_view'
