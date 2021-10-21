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
            'userImage':UserImage.objects.get(user=request.user)
        })


class Quest(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self, request, quest_id):
        answer = Answer.objects.filter(question_id = quest_id).order_by('dateTime')
        for ans in answer:
            ans.image = UserImage.objects.get(user_id=ans.user.id)
        return render(request, 'quest.html',{
            'quest':Question.objects.get(id=quest_id),
            'userImage':UserImage.objects.get(user=request.user),
            'answers':answer,
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
        form = SignUpForm(request.POST)
        fform = UserImageForm(request,request.FILES)
        if fform.is_valid() and form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                password=make_password(form.cleaned_data['password']),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'])
            if user is not None:
                UserImage.objects.create(
                    user=user,
                    image=fform.cleaned_data['image']
                )
                login(request,user)
                return redirect('index')
            else:
                user.delete()
        return render(request, 'signup.html',{'form':form,'fform':fform})