import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myCv.settings')

import django
django.setup()


from faker import Faker
fake = Faker()

from accounts.models import User
from groups.models import Group, GroupMember
from posts.models import Post
import random


uName = []
gName = []


def initializeList():
    for i in range(10):
        uName.append(fake.profile(fields=['username'])['username'])

    for i in range(10):
        gName.append(fake.sentence(nb_words=6))


def addUser():
    user = User.objects.get_or_create(username=random.choice(uName))[0]
    user.save()
    user.set_password(fake.word())
    user.save()
    return user


def addGroup():
    name = random.choice(gName)
    admin = addUser()
    desc = fake.paragraph(nb_sentences=3)
    group = Group.objects.get_or_create(name=name)[0]
    group.admin=admin
    group.desc=desc
    group.save()
    return group


def joinGroup():
    user = addUser()
    group = addGroup()
    gMember = GroupMember.objects.get_or_create(member=user, group=group)[0]
    gMember.save()


def addPost():
    message = fake.text(max_nb_chars=200, ext_word_list=None)
    publisher = addUser()
    group = addGroup()
    post = Post(publisher=publisher, group=group, message=message)
    post.save()


def populate(n):
    initializeList()
    for i in range(n):
        joinGroup()
        addPost()


if(__name__=='__main__'):
    print('\n Populating Fake DAta !!!')
    populate(15)
    print('\n Fake data is inserted...\n')
