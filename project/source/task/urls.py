
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from task.views import task_list, task_detail, TaskCreate, TaskEdit, task_comments,task_comment_add, count_likes, like_add

urlpatterns = [

    url(r'^$', task_list, name='task_list'),
    url(r'^(?P<pk>\d+)/detail/$', login_required(task_detail), name='task_detail'),
    url(r'^(?P<pk>\d+)/edit/$', login_required(TaskEdit.as_view()), name='task_edit'),
    url(r'^create/$', login_required(TaskCreate.as_view()), name='task_create'),
    url(r'^(?P<pk>\d+)/detail/comments/$', login_required(task_comments),  name='comments'),
    url(r'^(?P<pk>\d+)/detail/likes/$', login_required(count_likes), name='likes'),
    url(r'^(?P<pk>\d+)/detail/addlikes/$', login_required(like_add), name='add_like'),
    url(r'^(?P<pk>\d+)/addcomment/(?P<parent_id>\d+)/$', login_required(task_comment_add), name='comment_add'),

]
