from django.shortcuts import render
from django.views import generic
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import newPostForm
from django import forms
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# some login variables for this app
from django.conf import settings
LOGIN_URL = 'accounts:loginPage'

# Create your views here.


class listPost(LoginRequiredMixin, generic.ListView):
    login_url = LOGIN_URL
    model = Post
    template_name = 'posts/list_post.html'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['object_list'] = content['object_list'].filter(publisher=self.request.user)
        return content


class listUserPost(LoginRequiredMixin, generic.ListView):
    login_url = LOGIN_URL
    model = Post
    template_name = 'posts/list_post.html'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['object_list'] = content['object_list'].filter(publisher=User.objects.get(username=self.kwargs.get('slug')))
        content['userProfileName'] = User.objects.get(username=self.kwargs.get('slug')).username
        return content


class createPost(LoginRequiredMixin, generic.CreateView):
    login_url = LOGIN_URL
    model = Post
    template_name = 'posts/create_post.html'
    form_class = newPostForm

    def get_initial(self):
        return {
            'publisher':self.request.user,
        }

    # For Protection of publisher field from Dom Based Attack
    def form_valid(self,form):
        if(form.cleaned_data['publisher'] == self.request.user):
            return super().form_valid(form)
        else:
            print('not validdddddddddd/////////')
            return HttpResponse('<h1>Yeah Gotta... You Stupid Hacker... Anna Raskala... Mind It!!!')


class deletePost(LoginRequiredMixin, generic.DeleteView):
    login_url = LOGIN_URL
    model = Post
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy('posts:listPosts')
