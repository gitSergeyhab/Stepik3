from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Application, Company, Vacancy, UserSummary
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
class AddComForm(forms.ModelForm):
    """ форма для добавления и изменения Карточки компании """

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Сохранить'))

    class Meta:
        model = Company
        fields = ['name', 'logo', 'employee_count', 'location', 'description', 'owner']

        # !!! не разобрался как работают виджеты для  ImageField  и  IntegerField
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),

            # 'logo': forms.ImageField(),
            # 'employee_count': forms.IntegerField(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, }),
        }



# --------------- изменение вакансии --------------------
# class UpdVacForm(forms.ModelForm):
#     class Meta:
#         model = Vacancy
#         fields = ['title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description']
#
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'specialty': forms.Select(attrs={'class': 'form-control'}),
#             'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, }),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, }),
#         }


class UpdVacForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'company', 'specialty', 'level', 'salary_min', 'salary_max', 'skills', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, }),
        }

class UpdSummaryForm(forms.ModelForm):
    class Meta:
        model = UserSummary
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'readiness', 'salary', 'specialty',
                  'level', 'education', 'experience', 'portfolio', 'user']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'readiness': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'form-control'}),
            'education': forms.Select(attrs={'class': 'form-control'}),
            # 'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, }),
            'portfolio': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, }),
        }
