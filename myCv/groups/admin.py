from django.contrib import admin
from .models import Group, GroupMember

# Register your models here.

class GroupMemberTabularInline(admin.TabularInline):
    model = GroupMember


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [
        GroupMemberTabularInline,
    ]
