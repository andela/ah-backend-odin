"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include

from authors.apps.authentication.views import(
    password_reset,
    reset_password,
    change_passowrd,
)

app_name = "authentication"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authors.apps.authentication.urls')),
    path('api/articles/', include('authors.apps.articles.urls')),
    path('api/articles/', include('authors.apps.reporter.urls')),
    re_path(r'^api/set_password/complete/', change_passowrd, name='change_passowrd'),
    re_path(r'^api/password_reset/', password_reset, name='password'),
    re_path(r'^api/reset_password/', reset_password, name='reset_password'),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
