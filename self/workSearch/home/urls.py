"""workSearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^setPassword/', views.setPassword),
    url(r'^index/', views.index),
    url(r'^workPush/', views.workPush),
    url(r'^showResult/(?P<page>\d*)', views.showResult),
    url(r'^myWorkPush/', views.myWorkPush),
    url(r'^mySubscribe/', views.mySubscribe),
    url(r'^logout/', views.logout),
    url(r'^setSubscribe/', views.setSubscribe),
    url(r'^getSubscribe/', views.getSubscribe),
]
