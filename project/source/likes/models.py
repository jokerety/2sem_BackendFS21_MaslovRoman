# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from task.models import Task


class Like(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='likes',
        verbose_name=u'Автор')

    is_active = models.BooleanField(default=True, verbose_name=u'Лайк нажат')

    task = models.ForeignKey(
        Task,
        related_name='likes',
        verbose_name=u'Задание')

    class Meta:
        verbose_name = u' Лайк'
        verbose_name_plural = u'Лайки'




