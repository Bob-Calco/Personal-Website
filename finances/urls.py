from django.conf.urls import url

from . import views

app_name = 'finances'
urlpatterns = [
  url(r'^$', views.home, name="home"),
  url(r'^transactions/$', views.transactions, name="transactions"),
  url(r'^transaction/add/$', views.transaction, name="add_transaction"),
  url(r'^transaction/(?P<number>[0-9]+)', views.transaction, name="edit_transaction"),
  url(r'^categories/$', views.categories, name="categories"),
  url(r'^balance/$', views.balance, name="balance"),
  url(r'^searchterms/$', views.search_terms, name="search_terms"),
]
