from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog, Comment
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from . import forms
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import timezone

# LOGIN imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.


class index(TemplateView):
    template_name = 'blog/index.html'

class blogList(ListView):
    model = Blog
    template_name = 'blog/blogList.html'
    context_object_name = 'blogList'


@method_decorator(login_required, name='dispatch')
class userBlogList(ListView):
    model = Blog
    template_name = 'blog/userBlogList.html'
    context_object_name = 'blogList'


@method_decorator(login_required, name='dispatch')
class userDraftList(ListView):
    model = Blog
    template_name = 'blog/userDraftList.html'
    context_object_name = 'blogList'



def userCreate(request):
    form = forms.registrationForm()

    if(request.method == 'POST'):
        form = forms.registrationForm(request.POST)
        if(form.is_valid):
            print('validddddddd\n\n\n\n')
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect(reverse('blog:loginPage'))
        else:
            return HttpResponse(user.errors)
    else:
        return render(request, 'blog/userRegister.html', {'form':form})


def userLogin(request):
    if(request.method == 'POST'):
        Username = request.POST.get('username')
        Pass = request.POST.get('password')
        user = authenticate(username=Username, password=Pass)
        print('\nhello : ',str(user),'\n')
        if(user):
            if(user.is_active):
                login(request,user)
                return HttpResponseRedirect(reverse('blog:userBlogListPage'))
        else:
            return HttpResponse('Invalid User or Password')
    else:
        return render(request, 'blog/login.html')


@login_required
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:loginPage'))


def createBlog(request):
    if(request.user.is_authenticated):
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
    else:
        return HttpResponseRedirect(reverse('blog:loginPage'))


# class displayBlog(DetailView):
#     model = Blog
#     template_name = 'blog/blogDisplay.html'
#     context_object_name = 'blog'


def displayBlog(request, pk):
    blog = Blog.objects.get(pk=pk)
    if(blog.published_date!=None or request.user.is_superuser or request.user==blog.authorName):
        commentForm = forms.createComment()
        if(request.method == 'POST'):
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


@method_decorator(login_required, name='dispatch')
class updateBlog(UpdateView):
    model = Blog
    fields = ['title','content']
    template_name = 'blog/blogUpdate.html'
    success_url = reverse_lazy('blog:userBlogListPage')

    def get(self, request, pk, *args, **kwargs):
        if(request.user == Blog.objects.get(pk=pk).authorName):
            return super().get(request, *args, **kwargs)
        else:
            raise Http404('Page not found')


@method_decorator(login_required, name='dispatch')
class deleteBlog(DeleteView):
    model = Blog
    template_name = 'blog/blogDelete.html'
    success_url = reverse_lazy('blog:userBlogListPage')

    def get(self, request, pk, *args, **kwargs):
        if(request.user == Blog.objects.get(pk=pk).authorName or request.user.is_superuser):
            return super().get(request, *args, **kwargs)
        else:
            raise Http404('Page not found')


@method_decorator(login_required, name='dispatch')
class deleteComment(DeleteView):
    model = Comment
    success_url = ''

    def get(self, request, pk, *args, **kwargs):
        if(request.user.is_superuser or request.user==Comment.objects.get(pk=pk).post.authorName):
            self.success_url = reverse_lazy('blog:blogDisplayPage', kwargs={'pk':Comment.objects.get(pk=pk).post.id})
            return super().post(request, *args, **kwargs)
        else:
            raise Http404('Page not found')

    # def get(self, request, pk, *args, **kwargs):
    #     self.pk = pk
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(pk)
    #     context['pk'] = pk
    #     return context
