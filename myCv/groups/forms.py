from django import forms
from .models import Group


class createGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name','admin','desc']
        widgets = {
            'admin':forms.TextInput(attrs={'hidden':True,'readonly':True}),
        }
        labels = {
            'admin':'',
        }
