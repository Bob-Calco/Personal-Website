from django.conf.urls import url

from . import views

app_name = 'finances'
urlpatterns = [
  url(r'^$', views.home, name="home"),

  url(r'^transactions/$', views.transactions, name="default_transactions"),
  url(r'^transactions/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.transactions, name="transactions"),
  url(r'^transaction/add/$', views.transaction, name="add_transaction"),
  url(r'^transaction/(?P<number>[0-9]+)/delete/$', views.delete_transaction, name="delete_transaction"),
  url(r'^transaction/(?P<number>[0-9]+)/$', views.transaction, name="edit_transaction"),

  url(r'^categories/$', views.categories, name="categories"),
  url(r'^category/(?P<number>[0-9]+)/$', views.category, name='category'),
  url(r'^category/add/(?P<is_income>[0-1])/$', views.add_category, name='add_category'),
  url(r'^category/add/(?P<is_income>[0-1])/(?P<specification_of>[0-9]+)/$', views.add_category, name='add_specification'),
  url(r'^category/(?P<number>[0-9]+)/delete/$', views.delete_category, name='delete_category'),

  url(r'^balance/$', views.balance, name="default_balance"),
  url(r'^balance/(?P<year>[0-9]{4})/$', views.balance, name='balance'),
  url(r'^balance/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.balance_edit, name='balance_edit'),

  url(r'^searchterms/$', views.search_terms, name="search_terms"),

  url(r'^year-table/$', views.year_table, name="default_year_table"),
  url(r'^year-table/(?P<year>[0-9]{4})/$', views.year_table, name="year_table"),
]
