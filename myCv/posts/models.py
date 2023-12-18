from django.db import models
# import misaka
from groups.models import Group
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Post(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postPublisher')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='groupPost')
    message = models.TextField()
    message_html = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('posts:listPosts')

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        # self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-createdAt']
