from django.urls import path
from . import views

app_name = 'groups'



urlpatterns = [
    path('create/', views.createGroup.as_view(), name='createGroup'),
    path('list/', views.listGroup.as_view(), name='listGroup'),
    path('posts/in/<slug>', views.detailGroup.as_view(), name='detailGroup'),
    path('delete/<slug>/', views.deleteGroup.as_view(), name='deleteGroup'),
    path('join/<slug>/', views.joinGroup, name='joinGroup'),
    path('leave/<slug>', views.leaveGroup, name='leaveGroup'),
    path('list/created/', views.listCreatedGroup.as_view(), name='listCreatedGroup'),
    path('list/joined/', views.listJoinedGroup.as_view(), name='listJoinedGroup'),
]
