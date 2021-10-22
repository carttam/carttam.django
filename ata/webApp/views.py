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
from datetime import datetime
from .models import *
from datetime import datetime
from .forms import *

# Create your views here.
class Index(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        return render(request, 'index.html',{
            'quest':Question.objects.all().order_by('-dateTime'),
        })


class Quest(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self, request, quest_id, form = None):
        return render(request, 'quest.html',{
            'quest':Question.objects.get(id=quest_id),
            'answers':Answer.objects.filter(question__id=quest_id),
            'form':form
        })


    @method_decorator(login_required(login_url='/login'))
    def post(self, request, quest_id):
        form = AnswerForm(request.POST)
        if form.is_valid():
            ans = Answer.objects.create(
                user=request.user,
                answer=form.cleaned_data['answer'],
                question=get_object_or_404(Question,id=quest_id),
                dateTime=datetime.now()
            )
            if ans is not None:
                return redirect('quest',quest_id=quest_id)
        return self.get(request, quest_id, form)

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
    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        return render(request,'ask.html')


    @method_decorator(login_required(login_url='/login'))
    def post(self, request):
        form = AskForm(request.POST)
        if form.is_valid():
            q = Question.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                user=request.user,
                dateTime=datetime.now()
            )
            if q is not None:
                return redirect('index')
        return render(request,'ask',{'form':form})


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