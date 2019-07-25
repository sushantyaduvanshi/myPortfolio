from django.db import models
from django.contrib.auth import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class User(models.User):
    def __str__(self):
        return '@'+self.username

    # def get_absolute_url(self):
    #     return reverse(settings.LOGIN_URL)
