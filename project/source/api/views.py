# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from jsonrpc import jsonrpc_method
from core.models import User
from categories.models import *
from django.core.serializers import serialize
from django.db.models import Q
from django.core.files.base import ContentFile
import json
from core.models import UserFile
import base64
# Create your views here.


@jsonrpc_method('file_upload')
def upload_user_file(request, file_name, file_content):
    new_file = UserFile()
    new_file.owner = User.objects.get(id=1)
    new_file.file_name = file_name
    key = UserFile.generate_key(file_name, request.user.id)
    new_file.file_content.save(key, ContentFile(base64.b64decode(file_content.encode('utf-8'))))
    new_file.file_key = key
    new_file.file_mime = UserFile.file_buffer_mime(base64.b64decode(file_content.encode('utf-8')))
    new_file.save()
    return True
