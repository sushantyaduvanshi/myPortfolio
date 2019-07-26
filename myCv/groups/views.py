from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Group, GroupMember
from .forms import createGroupForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

# some login variables for this app
from django.conf import settings
LOGIN_URL = 'accounts:loginPage'


# Create your views here.
# GROUP VIEWS

class createGroup(LoginRequiredMixin, generic.CreateView):
    login_url = LOGIN_URL
    model = Group
    form_class = createGroupForm
    template_name = 'groups/create_group.html'

    def get_initial(self):
        return {
            'admin':self.request.user
        }

    def form_valid(self, form):
        if(form.cleaned_data['admin'] == self.request.user):
            return super().form_valid(form)
        else:
            return HttpResponse("<h2><em>Gott'a.... You Bloody Hacker!!!</em></h2>")


class listGroup(LoginRequiredMixin, generic.ListView):
    login_url = LOGIN_URL
    model = Group
    template_name = 'groups/list_group.html'


class listCreatedGroup(LoginRequiredMixin, generic.ListView):
    login_url = LOGIN_URL
    model = Group
    template_name = 'groups/list_created_group.html'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['object_list'] = content['object_list'].filter(admin=self.request.user)
        return content


class listJoinedGroup(LoginRequiredMixin, generic.ListView):
    login_url = LOGIN_URL
    model = Group
    template_name = 'groups/list_joined_group.html'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['object_list'] = content['object_list'].filter(members=self.request.user)
        return content


class detailGroup(LoginRequiredMixin, generic.DetailView):
    login_url = LOGIN_URL
    model = Group
    template_name = 'groups/detail_group.html'


class deleteGroup(LoginRequiredMixin, generic.DeleteView):
    login_url = LOGIN_URL
    model = Group
    template_name = 'groups/delete_group.html'
    success_url = reverse_lazy('groups:listGroup')

    # For authenticating and avoiding csrf_token hijacking
    def post(self, request, slug):
        if(request.user == Group.objects.get(slug=slug).admin):
            super().post(request, slug)
            return HttpResponseRedirect(self.success_url)
        else:
            raise Http404


@login_required(login_url=LOGIN_URL)
def joinGroup(request, slug):
    group = Group.objects.get(slug=slug)
    gMember = GroupMember(member=request.user, group=group)
    gMember.save()
    return HttpResponseRedirect(reverse('groups:detailGroup',kwargs={'slug':group.slug}))


@login_required(login_url=LOGIN_URL)
def leaveGroup(request, slug):
    group = Group.objects.get(slug=slug)
    gMember = GroupMember.objects.filter(member=request.user, group=group)
    gMember.delete()
    return HttpResponseRedirect(reverse('groups:detailGroup',kwargs={'slug':group.slug}))
