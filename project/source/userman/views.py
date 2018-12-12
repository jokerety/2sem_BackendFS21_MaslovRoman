# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from core.models import User
from django.http.response import HttpResponseNotFound, JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def userman (request):
    return HttpResponse ('This is userman')


@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_json = []
        for user in users:
            users_json.append({
                'id': user.id,
                'login': user.username,
            })
        return JsonResponse(users_json, safe=False)
    elif request.method == 'POST':
        return HttpResponse('Wrong request method')