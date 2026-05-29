from django import forms
from .models import Support,AnswerSupport

class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['title']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['user_id']
