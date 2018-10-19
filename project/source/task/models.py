# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from categories.models import Category
from core.models import User, UserFile
# Create your models here.


class TaskQuerySet (models.QuerySet):

    def annotate_everything(self):
        qs = self.filter(is_finished=False).select_related('auth')
        qs = qs.prefetch_related('categories', 'likes', 'likes__author')
        return qs

    def get_stats(self):
        return self.aggregate(tasks_count=models.Count('id'))


class Task(models.Model):

    auth = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tasks',
        verbose_name=u'Автор'
    )
    categories = models.ManyToManyField(Category, blank=True, related_name='tasks', verbose_name=u'Категории')
    name = models.CharField(max_length=255, verbose_name=u'Имя задания')
    is_finished = models.BooleanField(default=False, verbose_name=u'Задание завершено')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    prescription = models.TextField(max_length=4096, verbose_name=u'Описание')
    usertask = models.ManyToManyField(User, blank=True, related_name='users', verbose_name=u'Пользователи')
    is_published = models.BooleanField(default=True)
    viewcount = models.IntegerField(default=0)
    objects = TaskQuerySet.as_manager()
    file = models.ManyToManyField(UserFile)

    class Meta:
        verbose_name = u'Задание'
        verbose_name_plural = u'Задания'
        ordering = 'name', 'id'

    def __unicode__(self):
        return self.name

