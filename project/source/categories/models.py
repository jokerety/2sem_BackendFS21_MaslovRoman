# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=4096, verbose_name=u'Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    updated = models.DateTimeField(auto_now=True,verbose_name='Updated date')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    image = models.ImageField(verbose_name='Картинка', name='image', blank=True, upload_to='categories_pic')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'
        ordering = 'name', 'id'

