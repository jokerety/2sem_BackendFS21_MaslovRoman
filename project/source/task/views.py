# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import Task
# Create your views here.
def task_list(request):

    context = {
        'tasks': Task.objects.all()
    }

    return render(request, 'tasks/tasks_list.html', context)


def task_detail(request, pk=None):

    task =  get_object_or_404(Task, id=pk)

    context = {

        'task': task
    }
    return render(request, 'tasks/tasks_detail.html', context)

