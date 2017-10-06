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

  # CURRENT PROGRESS #

  url(r'^balance/$', views.balance, name="default_balance"),
  url(r'^balance/(?P<year>[0-9]{4})/$', views.balance, name='balance'),
  url(r'^balance/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.balance_edit, name='balance_edit'),

  url(r'^balance/items/$', views.balance_items, name='balance_items'),
  url(r'^balance/items/add/$', views.upsert_balance_item, name='add_balance_item'),
  url(r'^balance/items/(?P<pk>[0-9]+)/$', views.upsert_balance_item, name='edit_balance_item'),
  url(r'^balance/items/(?P<pk>[0-9]+)/delete/$', views.delete_balance_item, name='delete_balance_item'),

  url(r'^searchterms/$', views.search_terms, name="search_terms"),
  url(r'^searchterms/(?P<pk>[0-9]+)/$', views.search_term, name='search_term'),
  url(r'^searchterms/add/$', views.search_term, name='add_search_term'),
  url(r'^searchterms/(?P<pk>[0-9]+)/delete/$', views.delete_search_term, name='delete_search_term'),

  url(r'^datasets/$', views.datasets, name="datasets"),
  url(r'^datasets/(?P<pk>[0-9]+)/$', views.dataset, name='dataset'),
  url(r'^datasets/add/$', views.dataset, name='add_dataset'),
  url(r'^datasets/(?P<pk>[0-9]+)/delete/$', views.delete_dataset, name='delete_dataset'),

  url(r'^year-table/$', views.year_table, name="default_year_table"),
  url(r'^year-table/(?P<year>[0-9]{4})/$', views.year_table, name="year_table"),

  url(r'^upload-file/$', views.upload_file, name='upload_file'),
  url(r'^unprocessed-transactions/$', views.process_unprocessed_transactions, name='unprocessed_transactions'),
  url(r'^unprocessed-transactions/delete/(?P<pk>[0-9]+)/$', views.delete_unprocessed_transaction, name='delete_unprocessed_transaction'),
  url(r'^unprocessed-transactions/process/$', views.process_transaction, name='process_transactions'),
]
