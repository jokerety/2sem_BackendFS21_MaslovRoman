# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, get_object_or_404, HttpResponse
from .models import Task
from likes.models import Like
from comments.models import Comment
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.views.generic import UpdateView,CreateView
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error
from django.http import JsonResponse

def task_list(request):

    context = {
        'tasks': Task.objects.all()
    }

    return render(request, 'tasks/tasks_list.html', context)

def task_detail(request, pk=None):
    task = get_object_or_404(Task, id=pk)
    like_form = LikeForm()
    form = CommentForm()
    take_form = TakeTaskForm()
    close_form = CloseTaskForm()

    if request.method == 'POST':

        if 'take' in request.POST:
            take_form = TakeTaskForm(request.POST)
            if take_form.is_valid():
                task.usertask.add(request.user)
                task.save()

        elif 'close' in request.POST:
            close_form = CloseTaskForm(request.POST)
            if close_form.is_valid():
                task.is_finished = True
                task.save()

        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.task_id = pk
                comment.save()
                form = CommentForm()

    elif request.method == 'GET':
        Task.objects.filter(id=task.id).update(viewcount=models.F('viewcount') + 1)



    context ={
        'task': task,
        'likes': Like.objects.all().filter(is_active=True, task=task),
        'comment_form': form,
        'like_form' : like_form,
        'take_form' : take_form,
        'close_form' : close_form,
        'comments': Comment.objects.all().filter(is_archieve=False, task=task).order_by('created')
    }

    return render(request, 'tasks/tasks_detail.html', context)


class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name','prescription']

    def __init__(self,*args,**kwargs):
        super(EditTaskForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit','Сохранить'))


class TaskEdit (UpdateView):
    form_class = EditTaskForm
    context_object_name = 'task'
    template_name = 'tasks/tasks_edit.html'

    def get_queryset(self):
        return Task.objects.all()

    def get_success_url(self):
        return reverse('task:task_detail', kwargs={'pk': self.object.pk})


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name','prescription','categories']

    def __init__(self,*args,**kwargs):
        super(TaskForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit','Сохранить'))


class TaskCreate(CreateView):
    form_class = TaskForm
    context_object_name = 'task'
    template_name = 'tasks/tasks_create.html'

    def form_valid(self, form):
        form.instance.auth = self.request.user
        return super(TaskCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('task:task_detail', kwargs={'pk': self.object.pk})


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Добавить комментарий'))


def task_comments(request, pk=None):

    task = get_object_or_404(Task, id=pk)
    context = {
        'comments': task.task_comments.all().filter(is_archieve=False, comment=None).order_by('created')
    }

    return render(request, 'tasks/widjets/comments_all.html', context)


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Ответить'))


def count_likes(request, pk=None):

    task = get_object_or_404(Task, id=pk)

    context = {
        'likes': task.likes.filter(is_active=True)
    }
    return render(request, 'tasks/widjets/likes.html', context)


class LikeForm(ModelForm):
    class Meta:
        model = Like
        fields = []

    def __init__(self, *args, **kwargs):
        super(LikeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Лайкнуть'))


class TakeTaskForm(forms.Form):
    class Meta:
        model = Task
        fields = []

    def __init__(self, *args, **kwargs):
        super(TakeTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit('take', 'Взять задание'))


class CloseTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = []

    def __init__(self, *args, **kwargs):
        super(CloseTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit('close', 'Закрыть задание'))


def like_add(request, pk=None):
    task = get_object_or_404(Task, id=pk)
    form = LikeForm(request.POST)
    if form.is_valid():
        if task.likes.filter(author=request.user).count() == 0:
            like = form.save(commit=False)
            like.author = request.user
            like.task = task
            like.save()
            return HttpResponse("OK")
        else:
            like = task.likes.get(author=request.user)
            like.is_active = not like.is_active
            like.save()
            return HttpResponse("OK")

    return HttpResponse("Failed")


def task_comment_add (request, pk=None, parent_id=None):
    task = get_object_or_404(Task, id=pk)
    parent = get_object_or_404(task.task_comments, id=parent_id)
    form = AddCommentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task_id = pk
            comment.comment = parent
            comment.save()
            form = AddCommentForm()

    context = {
        'comment_form': form,
    }
    return render(request, 'tasks/widjets/comment_add.html', context)


@csrf_exempt
def get_all_tasks(request):
    tasks = Task.objects.all()

    tasks_json = []
    for task in tasks:
        tasks_json.append({
            'id': task.id,
            'name': task.name,
            'description': task.prescription,
            'categories_id': [obj for obj in task.categories.values_list('id', flat=True)],
        })

    return JsonResponse(tasks_json, safe=False)








