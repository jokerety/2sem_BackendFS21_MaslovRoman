from django.conf.urls import url, include
from django.contrib import admin

from core.views import RegisterFormView,LoginFormView,LogoutView

urlpatterns = [

    url(r'^register/$', RegisterFormView.as_view(), name='register'),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]