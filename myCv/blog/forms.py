from django import forms
from django.contrib.auth.models import User
from .models import Blog, Comment
from django.contrib.auth.forms import UserCreationForm


class registrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password1']
        labels = {
            'username':'UserName',
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
