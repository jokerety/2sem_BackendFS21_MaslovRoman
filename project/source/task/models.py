# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from categories.models import Category
# Create your models here.


class Task(models.Model):

    auth = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tasks',
        verbose_name=u'Автор'
    )
    categories = models.ManyToManyField(Category, blank=True, related_name='tasks',verbose_name=u'Категории')
    name = models.CharField(max_length=255, verbose_name=u'Имя задания')
    is_archieve = models.BooleanField(default=False, verbose_name=u'Задание завершено')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    prescription = models.TextField(max_length=4096, verbose_name=u'Описание')


    class Meta:
        verbose_name = u'Задание'
        verbose_name_plural = u'Задания'
        ordering = 'name', 'id'

    def __unicode__(self):
        return self.name
