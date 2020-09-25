from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Application
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

'''
    written_username = models.CharField(max_length=32, verbose_name="Имя")
    written_phone = models.CharField(max_length=32, verbose_name="Телефон")
    written_cover_letter = models.TextField(verbose_name="Сопроводительное письмо")
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)
'''

# --------------- форма добавления отклтка на вакансию -----------------------

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
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        # fields = ['username', 'email', 'password1', 'password2']


# --------------- форма аутентификации -----------------------

class UserAutForm(AuthenticationForm):
    username = forms.CharField(label='введите имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
