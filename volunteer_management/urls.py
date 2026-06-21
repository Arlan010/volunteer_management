"""volunteer_management URL Configuration

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
from django.shortcuts import redirect
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static


def redirect_to_kz(request, path=""):
    path = path or ""
    return redirect(f"/kz/{path}", permanent=False)


urlpatterns = [
    path('', redirect_to_kz),
    re_path(r'^ru(?:/(?P<path>.*))?$', redirect_to_kz),
    path('kz/', include('main.urls')),
    path('kz/admin/', admin.site.urls),
    path('kz/account/', include('account.urls')),
    path('kz/organization/', include('organization.urls')),
    path('kz/volunteers/', include('volunteers.urls')),
    path('kz/news/', include('news.urls')),
    path('rosetta/', include('rosetta.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
