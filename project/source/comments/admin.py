# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Comment

# Register your models here.
@admin.register(Comment)
class TaskAdmin(admin.ModelAdmin):
    list_display = 'id','task','author','comment','created','updated'
    search_fields = 'task', 'author__username'
    list_filter = 'is_archieve',
    pass
