from django.urls import path
from . import views


app_name = 'posts'


urlpatterns = [
    path('', views.listPost.as_view(), name='listPosts'),
    path('by/<slug>/', views.listUserPost.as_view(), name='listUserPosts'),
    path('create/', views.createPost.as_view(), name='createPost'),
    path('delete/<pk>', views.deletePost.as_view(), name='deletePost'),
]
