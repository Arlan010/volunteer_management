from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Құпиясөз'),
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Құпиясөзді қайталаңыз'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'email','role','photo')
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control'}),
            'first_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Пайдаланушының аты')
        self.fields['first_name'].label = _('Аты')
        self.fields['email'].label = _('Электрондық пошта мекенжайы')
        self.fields['role'].label = _('Рөлі')
        self.fields['role'].required = True
        self.fields['photo'].label = _('Фото')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
