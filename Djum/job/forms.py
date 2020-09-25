from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Application, Company
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


# --------------- форма добавления отклика на вакансию -----------------------
class ApplicationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Записаться на пробный урок'))

    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter', 'vacancy', 'user']

        #  c {% crispy form "bootstrap4" %} в шаблоне это уже не нужно!!!
        # widgets = {
        #     'written_username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'written_phone': forms.TextInput(attrs={'class': 'form-control'}),
        #     'written_cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, }),
        #     'vacancy': forms.Select(attrs={'class': 'form-control'}),
        #     'user': forms.Select(attrs={'class': 'mb-3 form-control'}),
        # }


# --------------- форма регистрации -----------------------
class UserRegForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']



# --------------- форма аутентификации -----------------------
class UserAutForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# --------------- изменение компании --------------------
class EditComForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'employee_count', 'location', 'description', 'owner']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            # 'logo': forms.ImageField(),
            # 'employee_count': forms.IntegerField(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, }),
        }

