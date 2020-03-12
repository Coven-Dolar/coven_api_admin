"""coven URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet


urlpatterns = [
    path('', admin.site.urls),
    path('web/', include('apps.web.urls')),
    path('api/auth/', obtain_auth_token),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/blog/', include('apps.blog.urls')),
    path('api/v1/indicadores/', include('apps.indicadores.urls')),
    path('api/v1/devices', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
