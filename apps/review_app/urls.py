from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.index),
	url(r'^register$',views.register),
	url(r'^login$',views.login),
	url(r'^success$',views.success),
	url(r'^my_book/(?P<id>\d+)$',views.my_book),
	url(r'^add_book/(?P<id>\d+)$',views.add_book),
	url(r'^book_info/(?P<id>\d+)$',views.book_info),
	url(r'^add_review/(?P<id>\d+)$',views.add_review),
	url(r'^user_info/(?P<id>\d+)$',views.user_info),
	url(r'^delete/(?P<id>\d+)$',views.delete),
	url(r'^logout$',views.logout),


	]