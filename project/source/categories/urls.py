
from django.conf.urls import url, include
from django.contrib import admin

from categories.views import  categories_list, category_detail

urlpatterns = [

    url(r'^$', categories_list, name='categories_list'),
    url(r'^(?P<pk>\d+)/detail/$', category_detail, name='category_detail'),


]
