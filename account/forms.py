import re

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

REQUIRED_ERROR = _('Бұл өрісті толтыру міндетті.')
PHONE_PATTERN = re.compile(r'^\+?[\d\s().-]{10,20}$')
PASSWORD_ALLOWED_PATTERN = re.compile(r'^[A-Za-z\d!@#$%^&*()_+\-=\[\]{};:"\\|,.<>/?`~]+$')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Құпиясөз'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        error_messages={'required': REQUIRED_ERROR},
        help_text=_('Кемінде 8 таңба, бір үлкен әріп, бір кіші әріп, бір сан және бір арнайы таңба енгізіңіз.'),
    )
    password2 = forms.CharField(
        label=_('Құпиясөзді қайталаңыз'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        error_messages={'required': REQUIRED_ERROR},
    )

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'email', 'role', 'phone', 'photo')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'given-name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 777 123 45 67',
                'autocomplete': 'tel',
                'inputmode': 'tel',
                'pattern': r'\+?[\d\s().-]{10,20}',
            }),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'username': {
                'required': REQUIRED_ERROR,
                'unique': _('Бұл пайдаланушы аты бұрын тіркелген. Басқа атау енгізіңіз.'),
                'invalid': _('Пайдаланушы аты тек әріптерден, сандардан және @/./+/-/_ таңбаларынан тұра алады.'),
            },
            'first_name': {'required': REQUIRED_ERROR},
            'email': {
                'required': REQUIRED_ERROR,
                'invalid': _('Электрондық пошта форматын дұрыс енгізіңіз.'),
            },
            'role': {'required': REQUIRED_ERROR},
            'phone': {
                'required': REQUIRED_ERROR,
                'max_length': _('Телефон нөмірі тым ұзын.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Пайдаланушы аты')
        self.fields['first_name'].label = _('Аты-жөні')
        self.fields['email'].label = _('Электрондық пошта мекенжайы')
        self.fields['role'].label = _('Рөлі')
        self.fields['role'].choices = (
            ('', ' '),
            (1, _('Ерікті')),
            (2, _('Ұйым')),
        )
        self.fields['phone'].label = _('Телефон')
        self.fields['photo'].label = _('Фото')

        for field_name in ('username', 'first_name', 'email', 'role', 'phone'):
            self.fields[field_name].required = True

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if len(username) < 3:
            raise forms.ValidationError(_('Пайдаланушы аты кемінде 3 таңбадан тұруы керек.'))
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].strip()
        if len(first_name) < 2:
            raise forms.ValidationError(_('Аты-жөніңіз кемінде 2 таңбадан тұруы керек.'))
        return first_name

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if UserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('Бұл электрондық пошта бұрын тіркелген. Басқа пошта енгізіңіз.'))
        return email

    def clean_phone(self):
        phone = re.sub(r'\s+', ' ', self.cleaned_data['phone'].strip())
        digits = re.sub(r'\D', '', phone)

        if not PHONE_PATTERN.match(phone) or len(digits) < 10:
            raise forms.ValidationError(_('Телефон нөмірін дұрыс форматта енгізіңіз. Мысалы: +7 777 123 45 67.'))
        if len(set(digits)) == 1:
            raise forms.ValidationError(_('Телефон нөмірі дұрыс емес сияқты. Нақты нөмір енгізіңіз.'))

        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            return password

        errors = []
        if len(password) < 8:
            errors.append(_('Құпиясөз кемінде 8 таңбадан тұруы керек.'))
        if not PASSWORD_ALLOWED_PATTERN.match(password):
            errors.append(_('Құпиясөз тек ағылшын әріптерінен, сандардан және арнайы таңбалардан тұруы керек.'))
        if not re.search(r'[A-Z]', password):
            errors.append(_('Құпиясөзде кемінде бір үлкен ағылшын әрпі болуы керек.'))
        if not re.search(r'[a-z]', password):
            errors.append(_('Құпиясөзде кемінде бір кіші ағылшын әрпі болуы керек.'))
        if not re.search(r'\d', password):
            errors.append(_('Құпиясөзде кемінде бір сан болуы керек.'))
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>/?`~]', password):
            errors.append(_('Құпиясөзде кемінде бір арнайы таңба болуы керек.'))

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError(_('Құпиясөздер сәйкес келмейді.'))

        return password2
