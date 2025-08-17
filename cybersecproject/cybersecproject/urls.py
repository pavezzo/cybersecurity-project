"""
URL configuration for cybersecproject project.

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
import os

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve
from project.views import admin_panel_handler, index_handler, add_handler, create_user_handler, login_handler, view_handler, logout_handler


urlpatterns = [
    path("admin/", admin_panel_handler),
    path("login/", login_handler),
    path("logout/", logout_handler),
    path("add/", add_handler, name="add"),
    path("create/", create_user_handler, name="create"),
    path("view", view_handler, name="view"),
    path("", index_handler, name="index"),

    # directory listing
    re_path(r'^files/(?P<path>.*)$', serve, {
        'document_root': os.path.join(settings.BASE_DIR, ''),
        'show_indexes': True
    }),
]
