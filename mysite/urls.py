"""mysite URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^beheerder/', admin.site.urls),
    url(r'', include('PW.urls')),
    url(r'^groceries/', include('groceries.urls')),
    url(r'^scrum/', include('scrum.urls')),
    url(r'^finances/', include('finances.urls')),
    url(r'^support/', include('support.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^pss/', include('projectsunset.urls')),
    url(r'^pj/', include('pj.urls')),
    url(r'^overtime/', include('overtime_tracker.urls')),
]
