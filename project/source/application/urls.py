"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from . import settings
from django.conf.urls import url, include
from django.contrib import admin
from core.views import index
from likes.views import likes
from task.views import task_detail, task_list
from rating.views import rating
from userman.views import userman
from categories.views import  categories_list, category_detail
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url
from jsonrpc import jsonrpc_site
from api.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url (r'^$', index),
    url (r'^likes/$', likes),
    url(r'^rating/$', rating),
    url(r'^task/', include ('task.urls', namespace='task')),
    url(r'^userman/', userman),
    url(r'^categories/',include ('categories.urls', namespace='categories')),
    url(r'^', include ('core.urls', namespace='core')),
    url(r'^', include('social_django.urls')),
    url (r'^api/', jsonrpc_site.dispatch)
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

