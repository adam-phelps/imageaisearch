"""iais URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("images", views.get_user_images, name="images"),
    path("advanced_analysis", views.advanced_analysis, name="advanced_analysis"),
    path("upload_image", views.upload_image, name="upload_image"),
    path("get_image/<int:img_id>", views.get_image, name="get_image"),
    path("request_img_analysis", views.request_img_analysis, name="request_img_analysis"),
    path("get_img_analysis", views.get_img_analysis, name="get_img_analysis"),
    re_path(r'(?P<id>[0-9a-f]{32})', views.display_img_search, name="displayimgsearch"),
    re_path(r'(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', views.display_img_analysis, name="displayimgsearch")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
