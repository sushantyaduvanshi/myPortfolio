from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    authorName = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publishBlog(self):
        self.published_date = timezone.now()

    def __str__(self):
        return self.title+' : '+self.authorName.username


class Comment(models.Model):
    post = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    authorName = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    aproved = models.BooleanField(default=False)

    def aproveComment(self):
        self.aproved = True

    def __str__(self):
        return self.content
