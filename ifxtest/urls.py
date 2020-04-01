"""ifxdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from rest_framework import routers
from ifxtest import settings
from ifxtest.views import get_remote_user_auth_token


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path(r'ifxtest/djadmin/', admin.site.urls),
    path(r'ifxtest/api/', include(router.urls)),
    path(r'ifxtest/api/djvocab', include('djvocab.urls')),
    path(r'ifxtest/api/obtain-auth-token/', get_remote_user_auth_token),
    url(r'^ifxtest/.*$', TemplateView.as_view(template_name="index.html")),
]