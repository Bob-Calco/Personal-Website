from django.conf.urls import url

from . import views

app_name = 'overtime_tracker'
urlpatterns = [
  url(r'^$', views.home, name="home"),

  url(r'^gettoken/$', views.gettoken, name="gettoken"),
  url(r'^wait_for_processing/$', views.wait_for_processing, name='wait_for_processing'),
  url(r'^process_data/$', views.process_data, name="process_data"),

  url(r'^days/$', views.read_days, name="read_days"),
  url(r'^day/$', views.upsert_day, name="insert_day"),
  url(r'^day/(?P<pk>[0-9]+)/$', views.upsert_day, name="update_day"),
  url(r'^day/(?P<pk>[0-9]+)/delete/$', views.delete_day, name="delete_day"),

  url(r'^configs/$', views.read_configs, name='read_configs'),
  url(r'^config/$', views.upsert_config, name='insert_config'),
  url(r'^config/(?P<pk>[0-9]+)/$', views.upsert_config, name='update_config'),
  url(r'^config/(?P<pk>[0-9]+)/delete/$', views.delete_config, name='delete_config'),

  url(r'^vacation_hours/$', views.read_vacation_hours, name='read_vacation_hours'),
  url(r'^vacation_hours/add/$', views.upsert_vacation_hours, name='insert_vacation_hours'),
  url(r'^vacation_hours/(?P<pk>[0-9]+)/$', views.upsert_vacation_hours, name='update_vacation_hours'),
  url(r'^vacation_hours/(?P<pk>[0-9]+)/delete/$', views.delete_vacation_hours, name='delete_vacation_hours'),
]
