from django.db import models
from django.utils.text import slugify
import misaka
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='groupAdmin')
    slug = models.SlugField(allow_unicode=True)
    desc = models.CharField(max_length=255)
    desc_html = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def get_absolute_url(self):
        return reverse('groups:detailGroup',kwargs={'slug':self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        self.desc_html = misaka.html(self.desc)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-createdAt']


class GroupMember(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='groupMember')

    def __str__(self):
        return self.member.username

    class Meta:
        unique_together = ['member','group']
        ordering = ['-member']
