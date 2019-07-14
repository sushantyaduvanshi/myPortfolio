import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myCv.settings')

import django
django.setup()

from faker import Faker
from blog.models import Blog, Comment
from django.contrib.auth.models import User
import random

fake = Faker()


userList = ['Sushant','Singham','Gopal','Ritesh','Tabu','Lucky']

def addUser():
    user = User.objects.get_or_create(username=random.choice(userList))[0]
    user.set_password('myblogger')
    user.save()
    return user

def addBlog():
    aName = addUser()
    title = fake.word()
    content = fake.paragraph(nb_sentences=100, ext_word_list=None)
    blog = Blog.objects.get_or_create(authorName=aName, title=title, content=content)[0]
    blog.save()
    return [blog, random.randint(6,20)]

def addComment():
    post, n = addBlog()
    for i in range(n):
        content = fake.sentence()
        aName = random.choice(User.objects.all())
        comment = Comment.objects.get_or_create(authorName=aName, content=content, post=post)[0]
        comment.save()

def populate(n):
    for i in range(n):
        addComment()


if(__name__=='__main__'):
    print('\nPopulating fake data...\n')
    populate(12)
    print('Fake Data is Inserted... Plz check !!!\n')
