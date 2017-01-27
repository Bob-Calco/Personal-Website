from django.conf.urls import url

from . import views

app_name = 'PW'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/', views.about, name='about'),
    url(r'^projects/', views.projects, name='projects'),
    url(r'^memory/', views.memory, name='memory'),
]
