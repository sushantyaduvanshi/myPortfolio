from django import forms
from django.contrib.auth.models import User
from .models import Blog, Comment


class registrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']
        labels = {
            'username':'Enter Username',
            'email':'Enter Email Address',
            'password':'Provide a Password'
        }
        widgets = {
            'password':forms.PasswordInput,
        }


class createBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content']


class createComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content':''
        }
