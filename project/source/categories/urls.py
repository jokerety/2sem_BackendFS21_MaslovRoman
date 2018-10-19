
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from categories.views import  categories_list, category_detail, CategoryEdit, CategoryCreate, testfunc

urlpatterns = [

    url(r'^$', login_required(categories_list), name='categories_list'),
    url(r'^(?P<pk>\d+)/detail/$', login_required(category_detail), name='category_detail'),
    url(r'^(?P<pk>\d+)/edit/$', login_required(CategoryEdit.as_view()), name='category_edit'),
    url(r'^create/$', login_required(CategoryCreate.as_view()), name = 'category_create'),
    url (r'^test/$', testfunc),
]
