from django import contrib
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import *
from datetime import datetime
from .forms import *

# Create your views here.
class Index(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        return render(request, 'index.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html',{'form':LoginForm()})

    def post(self, request):
        message = False
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request=request, user=user)
                return redirect(request.GET['next'])
            message = 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.'
        return render(request, 'login.html',{'form':form,'message': message})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class Ask(View):
    def get(self, request):
        logout(request)
        return redirect('index')