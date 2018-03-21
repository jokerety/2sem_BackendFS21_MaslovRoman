
from django.conf.urls import url, include
from django.contrib import admin

from task.views import task_list,task_detail

urlpatterns = [

    url(r'^$', task_list, name='task_list'),
    url(r'^(?P<pk>\d+)/detail/$', task_detail, name='task_detail'),

]
