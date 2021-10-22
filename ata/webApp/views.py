from django import contrib
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.contrib.auth.hashers import make_password
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
        return render(request, 'index.html',{
            'quest':Question.objects.all().order_by('dateTime'),
        })


class Quest(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self, request, quest_id):
        return render(request, 'quest.html',{
            'quest':Question.objects.get(id=quest_id),
            'answers':Answer.objects.filter(question__id=quest_id)
        })

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


class Signup(View):
    def get(self,request):
        return render(request,'signup.html')


    def post(self,request):
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                password=make_password(form.cleaned_data['password']),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                photo=form.cleaned_data['photo'],
                email=form.cleaned_data['email'])
            if user is not None:
                login(request,user)
                return redirect('index')
        return render(request, 'signup.html',{'form':form})