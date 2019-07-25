from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog, Comment
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from . import forms
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

# LOGIN imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views

from django.conf import settings


# some login variables for this app
LOGIN_URL = 'blog:loginPage'
LOGIN_REDIRECT_URL = 'blog:userBlogListPage'


# Create your views here.


class index(TemplateView):
    template_name = 'blog/index.html'


class loginUser(LoginView):
    template_name = 'blog/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy(LOGIN_REDIRECT_URL)


class blogList(ListView):
    model = Blog
    template_name = 'blog/blogList.html'
    context_object_name = 'blogList'


# login_url is defined in settings.py
# via with django redirect to loginPage when login_required failed
class userBlogList(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL
    model = Blog
    template_name = 'blog/userBlogList.html'
    context_object_name = 'blogList'


class userDraftList(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL
    model = Blog
    template_name = 'blog/userDraftList.html'
    context_object_name = 'blogList'


class userCreate(CreateView):
    template_name = 'blog/userRegister.html'
    form_class = forms.registrationForm
    success_url = reverse_lazy('blog:loginPage')


@login_required(login_url=LOGIN_URL)
def createBlog(request):
    form = forms.createBlogForm()
    if(request.method == 'POST'):
        form = forms.createBlogForm(request.POST)
        if(form.is_valid()):
            blog = form.save(commit=False)
            blog.authorName = User.objects.get(id=request.POST.get('authorName'))
            blog.save()
            return HttpResponseRedirect(reverse('blog:userDraftListPage'))
        else:
            return HttpResponse(user.errors)
    else:
        return render(request, 'blog/blogCreate.html', {'form':form})




def displayBlog(request, pk):
    blog = Blog.objects.get(pk=pk)
    if(blog.published_date!=None or request.user.is_superuser or request.user==blog.authorName):
        commentForm = forms.createComment()
        if(request.method == 'POST'):
            if(request.user.is_authenticated):
                commentForm = forms.createComment(request.POST)
                if(commentForm.is_valid()):
                    comment = commentForm.save(commit=False)
                    comment.authorName = request.user
                    comment.post = blog
                    comment.save()
                    return HttpResponseRedirect(reverse('blog:blogDisplayPage', kwargs={'pk':pk}))
                else:
                    return HttpResponse(form.errors)
            else:
                return HttpResponseRedirect(reverse('blog:loginPage'))
        else:
            return render(request, 'blog/blogDisplay.html', {'blog':blog,'commentForm':commentForm})
    else:
        raise Http404('Page not found')



def publishBlog(request, pk):
    if(request.user.is_superuser):
        blog = Blog.objects.get(pk=pk)
        blog.publishBlog()
        blog.save()
        return HttpResponseRedirect(reverse('blog:blogListPage'))
    else:
        raise Http404('Page not found')


def aproveComment(request, pk):
    if(request.user.is_superuser or request.user==Comment.objects.get(pk=pk).post.authorName):
        C = Comment.objects.get(pk=pk)
        C.aproveComment()
        C.save()
        return HttpResponseRedirect(reverse('blog:blogDisplayPage', kwargs={'pk':Comment.objects.get(pk=pk).post.pk}))
    else:
        raise Http404('Page not found')


class updateBlog(LoginRequiredMixin, UpdateView):
    login_url = LOGIN_URL
    model = Blog
    fields = ['title','content']
    template_name = 'blog/blogUpdate.html'
    success_url = reverse_lazy('blog:userBlogListPage')

    def get(self, request, pk, *args, **kwargs):
        if(request.user == Blog.objects.get(pk=pk).authorName):
            return super().get(request, *args, **kwargs)
        else:
            raise Http404('Page not found')


class deleteBlog(LoginRequiredMixin, DeleteView):
    login_url = LOGIN_URL
    model = Blog
    template_name = 'blog/blogDelete.html'
    success_url = reverse_lazy('blog:userBlogListPage')

    def get(self, request, pk, *args, **kwargs):
        if(request.user == Blog.objects.get(pk=pk).authorName or request.user.is_superuser):
            return super().get(request, *args, **kwargs)
        else:
            raise Http404('Page not found')


class deleteComment(LoginRequiredMixin, DeleteView):
    login_url = LOGIN_URL
    model = Comment
    success_url = ''

    def get(self, request, pk, *args, **kwargs):
        if(request.user.is_superuser or request.user==Comment.objects.get(pk=pk).post.authorName):
            self.success_url = reverse_lazy('blog:blogDisplayPage', kwargs={'pk':Comment.objects.get(pk=pk).post.id})
            return super().post(request, *args, **kwargs)
        else:
            raise Http404('Page not found')

class test(TemplateView):
    template_name = 'blog/test.html'
