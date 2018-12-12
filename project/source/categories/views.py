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
from django.views.decorators.csrf import csrf_exempt


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
        return render(request, 'categories/categories_list.html', context)


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
        return Category.objects.all()

    def get_success_url(self):
        return reverse('categories:category_detail', kwargs={'pk': self.object.pk})


class CategoryCreate(CreateView):
    form_class = CategoryForm
    context_object_name = 'category'
    template_name = 'categories/category_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        category = form.save()
        publish_category(category)
        return super(CategoryCreate, self).form_valid(form)

    def get_success_url(self):

        return reverse('categories:category_detail', kwargs={'pk': self.object.pk})


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
    return render(request, 'categories/category_detail.html', context)


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


import requests
from application.settings import CENTRIFUGE_API_KEY


def publish_category(category):
    command = {
        "method": "publish",
        "params": {
            "channel": "public:screen-updates",
                "data": {
                    "category": serialize('json', [ category, ], )
                }
            }
    }
    api_key = CENTRIFUGE_API_KEY
    data = json.dumps(command)
    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + api_key}
    resp = requests.post("http://localhost:9000/api", data=data, headers=headers)
    print(resp.json())


@csrf_exempt
def get_all_categories(request):
    categories = Category.objects.all()

    categories_json = []
    for category in categories:
        categories_json.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'tasks_id': [obj for obj in category.tasks.values_list('id', flat=True)],
        })

    return JsonResponse(categories_json, safe=False)