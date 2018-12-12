# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect,JsonResponse
from core.models import User
from django.shortcuts import render,HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm as OldUserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from django.views.generic.base import View
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.views.decorators.csrf import csrf_exempt
import hashlib, json
from django.contrib.auth import login as loginUser, logout as logoutUser

class UserCreationForm(OldUserCreationForm):
    class Meta:
        model = User
        fields = ('username', )



class TrueRegister(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(TrueRegister, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'зарегистрироваться'))


class RegisterFormView(FormView):
    form_class = TrueRegister

    success_url = reverse_lazy("core:login")

    template_name = "core/register.html"

    def form_valid(self, form):

        form.save()
        return super(RegisterFormView, self).form_valid(form)


def index (request):
    return HttpResponse ('This is index')


class TrueLogin (AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(TrueLogin,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit','войти'))


class LoginFormView (FormView):
    form_class = TrueLogin

    template_name = "core/login.html"

    success_url = reverse_lazy("categories:categories_list")

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super (LoginFormView, self).form_valid(form)


@csrf_exempt
def login2(request):
    if request.method == 'GET':
        return HttpResponse('Use post')
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = AuthenticationForm(data=data)
        if form.is_valid():
            user = form.get_user()
            loginUser(request, user)
            return JsonResponse({
                'userId': user.pk,
                'token': generate_key(user.get_username())
            })
        else:
            return HttpResponse('Unauthorized', status=401)

@csrf_exempt
def logout(request):
    logoutUser(request)
    return JsonResponse({ 'status': 200 })


class LogoutView(View):
    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse_lazy("core:login"))


def home(request):
    context = {}
    template = 'core/home.html'
    return render(request, template, context)

def generate_key(filename):
    h = hashlib.new('md5')
    h.update(filename.encode('utf-8'))
    return h.hexdigest()