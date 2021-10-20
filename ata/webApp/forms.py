from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(min_length=4,max_length=255,required=True)
    password = forms.CharField(min_length=8,max_length=64,required=True)


    class Meta:
        model = User
