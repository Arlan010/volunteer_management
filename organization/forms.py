from django import forms
from django.contrib.auth import get_user_model

from .models import Project,Organization
from account.models import CustomUser

UserModel = get_user_model()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','end_date','number_of_volunteers','location','comment','category','photo']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'end_date' : forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}),
            'number_of_volunteers' : forms.TextInput(attrs={'class': 'form-control'}),
            'location' : forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control','rows':5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }
        exclude = ['organization_id']

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['title','content']
        exclude = ['user_id']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email')


