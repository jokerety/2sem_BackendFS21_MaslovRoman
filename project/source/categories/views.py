# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from .models import Category
from django import forms
from django.views.generic import UpdateView,CreateView
from django.urls import reverse_lazy
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db import models
from django.core.cache import caches
from likes.models import Like
from django.http import JsonResponse
cache = caches['default']
from jsonrpc import jsonrpc_method
import json
from django.core.serializers import serialize
from time import sleep


class CategoryListForm(forms.Form):

    sort = forms.ChoiceField(
        choices=(
            ('name', 'По алфавиту'),
            ('-name', 'С конца алфавита'),
            ('id', 'По порядку'),
            ('-created', 'По дате создания'),
        ),
        required=False
    )

    search = forms.CharField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(CategoryListForm, self).__init__(*args, **kwargs)
        self.fields['sort'].widget.attrs['class'] = 'form-control'
        self.fields['search'].widget.attrs['class'] = 'form-control'


@jsonrpc_method('categories.list')
def categories_list(request):

    categories = Category.objects.all()

    if request.method == 'GET':
        form = CategoryListForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data['sort']:
                categories = categories.order_by(data['sort'])
            if data['search']:
                categories = categories.filter(name__icontains=data['search'])
        context = {
            'categories': categories,
            'form': form,
        }
        return json.loads(serialize('json', categories))

    elif request.method == 'POST':
        return JsonResponse({'goto': "core:login"})


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name','description','image']

    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Сохранить'))
        self.helper.form_tag = False


class CategoryEdit(UpdateView):
    form_class = CategoryForm
    context_object_name = 'category'
    template_name = 'categories/category_edit.html'

    def get_queryset(self):
        return json.loads(serialize('json',Category.objects.all()))

    def get_success_url(self):
        #return JsonResponse({'goto': "categories:category_detail", "pk" : self.object.pk})
        return reverse('categories:category_detail', kwargs={'pk': self.object.pk})


class CategoryCreate(CreateView):
    form_class = CategoryForm
    context_object_name = 'category'
    template_name = 'categories/category_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CategoryCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('categories:category_detail', kwargs={'pk': self.object.pk})

@jsonrpc_method('category_detail')
def category_detail(request, pk=None):

    category = get_object_or_404(Category, id=pk)

    tasks = category.tasks.all()
    tasks = tasks.annotate_everything()

    if request.method == 'GET':
        form = TaskListForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data['sort']:
                tasks = tasks.order_by(data['sort'])
            if data['search']:
                tasks = tasks.filter(name__icontains=data['search'])

    for task in tasks:
        cache_key = 'post{}likescount'.format(task.id)
        likes_count = cache.get(cache_key)
        if likes_count is None:
            likes_count = Like.objects.filter(models.Q(task=task.id) & models.Q(is_active=True)).count()
            cache.set(cache_key,likes_count,10)
        task.likes_count = likes_count

    context = {
        'category': category,
        'tasks': tasks,
        'form': form,
    }
    return json.loads(serialize('json', context))


class TaskListForm(forms.Form):

    sort = forms.ChoiceField(
        choices=(
            ('name', 'По алфавиту'),
            ('-viewcount', 'По просмотрам'),
            ('-created', 'По дате создания'),
        ),
        required=False
    )

    search = forms.CharField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        self.fields['sort'].widget.attrs['class'] = 'form-control'
        self.fields['search'].widget.attrs['class'] = 'form-control'


def testfunc(request):
    title = Category.objects.last().name
    return JsonResponse({'category': title})

def mock():
    sleep(10)
    return 200