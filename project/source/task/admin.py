# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin (admin.ModelAdmin):

    list_display = 'name', 'auth'
    search_fields = 'name', 'auth__username'
    list_filter = 'is_archieve',
