from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class VolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'email', 'phone', 'photo')
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = _('Еріктінің аты-жөні')
        self.fields['email'].label = _('Email')
        self.fields['phone'].label = _('Телефон')
        self.fields['photo'].label = _('Профиль суреті')
        self.fields['photo'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.last_name = ''
        if commit:
            user.save()
            self.save_m2m()
        return user
