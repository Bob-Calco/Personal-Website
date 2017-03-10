from django.conf.urls import url

from . import views

app_name = 'support'
urlpatterns = [
    url(r'^(user/(?P<id>[0-9]+)/|)check-messages/$', views.check_messages, name="check_messages"),
    url(r'^$', views.inbox, name="inbox"),
    url(r'^user-overview/$', views.user_overview, name="user_overview"),
    url(r'^user/(?P<id>[0-9]+)/$', views.user, name="user"),
]
