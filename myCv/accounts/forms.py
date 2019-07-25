from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import models


class signupForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['username','password1','password2']
