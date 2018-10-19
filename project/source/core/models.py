# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import hashlib
import magic
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    pass


class UserFile(models.Model):
    file_content = models.FileField(upload_to='user_files/')
    file_mime = models.CharField(max_length=255)
    file_key = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)

    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(default=None, null=True)
    is_deleted = models.BooleanField(default=False, null=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_files')

    @staticmethod
    def generate_key(file_name, user_id):
        key = hashlib.md5()
        key.update("{}.{}".format(file_name, user_id).encode('utf-8'))
        return key.hexdigest()

    @staticmethod
    def file_buffer_mime(file_buffer):
        mime = magic.from_buffer(file_buffer, mime=True)
        return mime