from .models import Post
from django.forms import ModelForm
from django import forms


class newPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['message','publisher','group']
        widgets = {
            'publisher':forms.TextInput(attrs={'readonly':True,'hidden':True})
        }
        labels = {
            'publisher':'',
        }
