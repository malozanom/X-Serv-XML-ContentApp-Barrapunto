"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from cms_barrapunto import views

urlpatterns = [
    url(r'^cms_barrapunto/?$', views.show, name='Show the database content'),
    url(r'^cms_barrapunto/(\d+)$', views.entry, name='Show the selected page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'.*', views.error, name='Not found')
]
