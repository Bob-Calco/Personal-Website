from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

app_name = 'pj'
urlpatterns = [
 url(r'^$', TemplateView.as_view(template_name='pj/home.html'), name='home'),
 url(r'^programma/$', TemplateView.as_view(template_name='pj/schedule.html'), name='schedule'),
 url(r'^aanmelden/$', views.signup, name='signup'),
 url(r'^opkomst/$', views.view_turnout, name='view_turnout'),
 url(r'^routebeschrijving/$', TemplateView.as_view(template_name='pj/directions.html'), name='directions'),
]
