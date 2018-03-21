# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Category


# Create your views here.
def categories_list(request):
    context = {
        'categories': Category.objects.all()
    }

    return render(request, 'categories/categories_list.html', context)


def category_detail(request, pk=None):

    category =  get_object_or_404(Category, id=pk)

    context = {
        'category': category,
        'tasks': category.tasks.all().filter(is_archieve=False)
    }
    return render(request, 'categories/category_detail.html', context)
