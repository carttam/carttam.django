from django import forms
from django.db.models import fields
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=255, required=True)
    password = forms.CharField(min_length=8, max_length=64, required=True)

    class Meta:
        model = User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(min_length=4, max_length=255)
    password = forms.CharField(min_length=8, max_length=64)
    first_name = forms.CharField(required=True, min_length=3, max_length=80)
    last_name = forms.CharField(required=True, min_length=4, max_length=80)
    photo = forms.ImageField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class AnswerForm(forms.Form):
    answer = forms.CharField(required=True)

    class Meta:
        models = Answer
        fields = ['answer']


class AskForm(forms.Form):
    title = forms.CharField(required=True,max_length=255)
    description = forms.CharField(required=True)
    class Meta:
        models = Question