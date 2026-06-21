from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Organization, Project

UserModel = get_user_model()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'end_date', 'number_of_volunteers', 'location', 'comment', 'category', 'photo', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_volunteers': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Астана, Мәңгілік Ел даңғылы'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }
        error_messages = {
            'photo': {'required': _('Жобаға фото қосу міндетті.')},
            'latitude': {'invalid': _('Ендікті сан ретінде енгізіңіз.')},
            'longitude': {'invalid': _('Бойлықты сан ретінде енгізіңіз.')},
        }
        exclude = ['organization_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True
        self.fields['photo'].error_messages['required'] = _('Жобаға фото қосу міндетті.')
        self.fields['latitude'].label = _('Ендік')
        self.fields['longitude'].label = _('Бойлық')
        self.fields['latitude'].required = False
        self.fields['longitude'].required = False

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        if latitude is None or longitude is None:
            message = _('Картада көрсету үшін орынды картадан таңдаңыз немесе мекенжайды іздеңіз.')
            self.add_error('latitude', message)
            self.add_error('longitude', message)
        if latitude is not None and not -90 <= latitude <= 90:
            self.add_error('latitude', _('Ендік -90 мен 90 аралығында болуы керек.'))
        if longitude is not None and not -180 <= longitude <= 180:
            self.add_error('longitude', _('Бойлық -180 мен 180 аралығында болуы керек.'))

        return cleaned_data


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['title', 'content']
        exclude = ['user_id']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'email', 'phone', 'photo')
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        role = getattr(self.instance, 'role', None)
        if role == 1:
            self.fields['first_name'].label = _('Еріктінің аты-жөні')
        else:
            self.fields['first_name'].label = _('Координатордың аты-жөні')
        self.fields['photo'].label = _('Профиль суреті')
        self.fields['photo'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.last_name = ''
        if commit:
            user.save()
            self.save_m2m()
        return user
