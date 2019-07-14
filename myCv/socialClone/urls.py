from django.urls import path
from socialClone import views

app_name = 'socialClone'

urlpatterns = [
    path('', views.index.as_view(), name='indexPage')
]
