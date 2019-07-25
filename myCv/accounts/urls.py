from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns=[
    path('signup', views.signup.as_view(), name='signupPage'),
    path('accounts/login/', views.login.as_view(), name='loginPage'),
    path('logout', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logoutPage'),
]
