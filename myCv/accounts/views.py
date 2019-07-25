from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


# some login variables for this app
from django.conf import settings
LOGIN_URL = 'accounts:loginPage'
LOGIN_REDIRECT_URL = 'posts:listPosts'

# Create your views here.

class index(TemplateView):
    template_name = 'starSocialIndex.html'


class signup(CreateView):
    template_name = 'accounts/signup.html'
    form_class = forms.signupForm
    login_url = LOGIN_URL


class login(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy(LOGIN_REDIRECT_URL)
