from django.conf.urls import url, include
from django.contrib import admin

from core.views import RegisterFormView,LoginFormView,LogoutView, home, login2, logout

urlpatterns = [

    url(r'^register/$', RegisterFormView.as_view(), name='register'),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^logout/$',  logout, name='logout'),
    url(r'^home/$', home, name='home'),
    url(r'login2/$', login2),
]