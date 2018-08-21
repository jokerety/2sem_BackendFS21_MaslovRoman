# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings

from task.models import Task
from django.db import models

# Create your models here.


class Comment (models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='author_comment',
        verbose_name='Author name'
    )
    task = models.ForeignKey(
        Task,
        related_name='task_comments',
        verbose_name='Task'
    )
    text = models.TextField(
        max_length=4096,
        verbose_name='Comment text'
    )
    comment = models.ForeignKey(
        'self', blank=True,null=True,
        related_name='child_comments',
        verbose_name='parent comment'
    )
    is_archieve = models.BooleanField(
        default=False,
        verbose_name='Comment archieved'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Update date'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = 'task', 'author', 'id'

    def __unicode__(self):
        return str(self.id)