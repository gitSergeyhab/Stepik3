# from django.shortcuts import render
# from django.views import View

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm

from .models import Specialty, Company, Vacancy, Application
from .models import skillist
from random import shuffle
from .forms import ApplicationForm, UserRegForm, UserAutForm, AddComForm

title = 'Джуманджи'
shuffle(skillist)


class MainView(ListView):
    model = Specialty
    template_name = 'job/index.html'
    context_object_name = 'main_specialty'
    extra_context = {'title': title, 'skillist': skillist[:5]}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['company'] = Company.objects.all()
        return context


# – Вакансии по специализации /vacancies/cat/frontend
class ListVacSpecialties(ListView):
    template_name = 'job/vacancies.html'
    context_object_name = 'vacancies'
    extra_context = {'title': title}

    # !!! =self.kwargs['slug'] - украдено из интернотов и работает, но как именно - НЕ понимаю !!!
    def get_queryset(self):
        return Vacancy.objects.filter(specialty__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_specialty'] = Specialty.objects.filter(slug=self.kwargs['slug'])
        return context


# – Все вакансии списком   /vacancies
class ListVacancies(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'job/vacancies.html'
    extra_context = {'title': title}
    # paginate_by = 8


# – Одна вакансия /vacancies/22
class OneVacancy(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'job/vacancy.html'
    extra_context = {'title': title, }


# – Карточка компании  /companies/345
class CardCompany(ListView):
    template_name = 'job/vacancies.html'
    context_object_name = 'vacancies'
    extra_context = {'title': title}

    def get_queryset(self):
        return Vacancy.objects.filter(company__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_company'] = Company.objects.filter(pk=self.kwargs['pk'])
        return context


class Companies(ListView):
    model = Company
    template_name = 'job/companies.html'
    context_object_name = 'companies'
    extra_context = {'title': title, }


# ----------------------- 4 week --------------------

class CreateApplication(CreateView):
    form_class = ApplicationForm
    template_name = 'job/vacancy.html'
    extra_context = {'title': title, }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = Vacancy.objects.get(pk=self.kwargs['pk'])
        context['application'] = Application.objects.all()

        return context


# ------------------- registrations -------------------
class MySignupView(CreateView):
    # form_class = UserCreationForm
    form_class = UserRegForm
    success_url = 'login'
    template_name = 'signup.html'
    extra_context = {'title': title, }


# ------------------- registrations -------------------

# class MyLoginView(LoginView):
#     redirect_authenticated_user = True
#     template_name = 'login.html'
#     extra_context = {'title': title, }

# !!! через класс красиво не получилось, а в функции с трудом понимаю, что вообще происходит
def my_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserAutForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserAutForm()
    return render(request, 'login.html', {'form': form, 'title': title, })


# ----------------------- user profil ----------------------------

'''
– Моя компания /mycompany
– Мои вакансии /mycompany/vacancies
– Одна моя вакансия  /mycompany/vacancies/<vacancy_id>
'''


class EditCompany(CreateView):
    form_class = AddComForm
    template_name = 'job/company-edit.html'
    extra_context = {'title': title, }


class AddCompany(CreateView):
    model = Company
    form_class = AddComForm
    template_name = 'job/company-edit.html'
    extra_context = {'title': title, }

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.save()
    #     return redirect('/job/company-edit/')


class UpdateComp(UpdateView):
    model = Company
    form_class = AddComForm
    template_name = 'job/company-upd.html'
    extra_context = {'title': title, }

    # def get_success_url(self):
    #     return reverse('companies')


class MyVacancies(ListView):
    model = Vacancy
    template_name = 'job/vacancy-list.html'
    context_object_name = 'vacancies'
    extra_context = {'title': title}

    def get_queryset(self):
        return Vacancy.objects.filter(company__owner=self.request.user)


class UserProf(DetailView):
    template_name = 'job/user_prof.html'
    context_object_name = 'user_'
    extra_context = {'title': title}

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
