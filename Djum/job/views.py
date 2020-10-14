# from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm

from .models import Specialty, Company, Vacancy, Application, UserResume
from .data import skillist
from random import shuffle
from .forms import ApplicationForm, UserRegForm, UserAutForm, CompanyForm, VacancyForm, ResumeForm

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
class ListVacSpecialtiesView(ListView):
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
class ListVacanciesView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'job/vacancies.html'
    extra_context = {'title': title}
    # paginate_by = 8


# – Одна вакансия /vacancies/22
class OneVacancyView(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'job/vacancy.html'
    extra_context = {'title': title, }


# – Карточка компании  /companies/345
class CardCompanyView(ListView):
    template_name = 'job/vacancies.html'
    context_object_name = 'vacancies'
    extra_context = {'title': title}

    def get_queryset(self):
        return Vacancy.objects.filter(company__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_company'] = Company.objects.filter(pk=self.kwargs['pk'])
        return context


class CompaniesView(ListView):
    model = Company
    template_name = 'job/companies.html'
    context_object_name = 'companies'
    extra_context = {'title': title, }


# ----------------------- 4 week --------------------

class CreateApplicationView(View):

    def get(self, request, pk):
        form = ApplicationForm()
        form.fields['vacancy'].queryset = Vacancy.objects.filter(pk=pk)
        form.fields['vacancy'].initial = Vacancy.objects.get(pk=pk)
        form.fields['user'].queryset = User.objects.filter(pk=request.user.pk)
        form.fields['user'].initial = User.objects.get(pk=request.user.pk)

        return render(request, 'job/vacancy.html', context={
            'form': form,
            'vacancy': Vacancy.objects.get(pk=self.kwargs['pk']),
            'title': title,
            'flag_appl': 1,
        })

    def post(self, request, pk):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            new_appl = form.save()
            return redirect('sent', pk)
        return render(request, 'job/vacancy.html', context={'form': form, })


# ------------------- регистрация и вход -------------------
class MySignupView(CreateView):
    form_class = UserRegForm
    success_url = 'login'
    template_name = 'signup.html'
    extra_context = {'title': title, }


# ???!!! через класс красиво не получилось, а в функции с трудом понимаю, что вообще происходит
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


# ----------------------- добавление и редактирование компании ----------------------------
class AddCompanyView(View):

    def get(self, request):
        form = CompanyForm()
        form.fields['owner'].initial = request.user
        return render(request, 'job/company-edit.html', context={'form': form, 'title': title, })

    def post(self, request):
        form = CompanyForm(request.POST)
        if form.is_valid():
            new_company = form.save()
            return redirect(new_company)
        return render(request, 'job/company-edit.html', context={'title': title, 'form': form, })


class UpdateCompanyView(UpdateView):
    """   редактирование компании    """
    model = Company
    form_class = CompanyForm
    template_name = 'job/company-upd.html'
    extra_context = {'title': title, }


class MyVacanciesView(ListView):
    """ лист вакансий компаний аутифиц. пользователя с компанией """
    # раз есть get_queryset   model = Vacancy    можно удалить
    model = Vacancy
    template_name = 'job/vacancy-list.html'
    context_object_name = 'vacancies'
    extra_context = {'title': title}

    def get_queryset(self):
        return Vacancy.objects.filter(company__owner=self.request.user)


# ----------------------- user profile ----------------------------
class UserProfileView(DetailView):
    """ окно при нажатии на "компания" в выпадающем меню зарег пользователя,
    у которого нет компании (ссылка на допввление компании) """
    model = User
    template_name = 'job/user_prof.html'
    # context_object_name   на самом деле не требуется и не используется - используется   user  и  request.user
    context_object_name = 'curuser'
    extra_context = {'title': title}



class DemoCompView(View):
    """ окно при нажатии на "компания" в выпадающем меню зарег пользователя,
    у которого нет компании (ссылка на допввление компании) """

    def get(self, request, *args, **kwargs):
        return render(request, 'job/my_demo_company.html', context={'title': title})


# ----------------------- добавление и редактирование вакансии ----------------------------
class AddVacancyView(View):

    def get(self, request):
        form = VacancyForm()
        # оставляет селект с 1-пунктом (без initial по умолчанию выбирается: ---------):
        form.fields['company'].queryset = Company.objects.filter(owner__pk=request.user.pk)
        # делает это пункт выбранным (без queryset остается возможность выбора из всего списка)
        form.fields['company'].initial = Company.objects.get(owner__pk=request.user.pk)

        # form = UpdVacForm(initial={'company': Company.objects.get(owner__pk=request.user.pk)})
        return render(request, 'job/vacancy-add.html', context={'title': title, 'form': form})

    def post(self, request):
        form = VacancyForm(request.POST)
        if form.is_valid():
            new_vacancy = form.save()
            return redirect(new_vacancy)
        return render(request, 'job/vacancy-add.html', context={'title': title, 'form': form})



class UpdateVacancyView(UpdateView):
    """ правка вакансии """
    model = Vacancy
    form_class = VacancyForm
    template_name = 'job/vacancy-upd.html'
    extra_context = {'title': title,}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_vacancy'] = Vacancy.objects.get(pk=self.kwargs['pk'])
        return context



# ----------------------- Поиск ----------------------------
class SearcherView(ListView):
    context_object_name = 'vacancies'
    template_name = 'job/searcher.html'
    extra_context = {'title': title, 'skillist': skillist[:3]}

    def get_queryset(self):
        return Vacancy.objects.filter(
            Q(title__icontains=self.request.GET.get('s')) | Q(description__icontains=self.request.GET.get('s')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_search'] = self.request.GET.get('s')
        return context


# ----------------------- добавление и редактирование резюме ----------------------------
class AddUserResumeView(View):
    def get(self, request):
        form = ResumeForm()
        form.fields['user'].initial = request.user

        return render(request, 'job/resume-edit.html', context={'form': form, 'title': title})
    def post(self, request):
        form = ResumeForm(request.POST)
        if form.is_valid():
            new_resume = form.save()
            return redirect('profile', request.user.pk)
        return render(request, 'job/resume-edit.html', context={'form': form, 'title': title})


class UpdUserResumeView(View):
    def get(self, request, pk):
        resume = UserResume.objects.get(pk=pk)
        form = ResumeForm(instance=resume)
        return render(request, 'job/resume-edit.html', context={'form': form, 'title': title})

    def post(self, request, pk):
        resume = UserResume.objects.get(pk=pk)
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            resume = form.save()
            return redirect('profile', request.user.pk)
        return render(request, 'job/resume-edit.html', context={'form': form, 'title': title})


class DemoResumeView(View):
    """ окно при нажатии на "компания" в выпадающем меню зарег пользователя,
    у которого нет компании (ссылка на допввление компании) """
    def get(self, request, *args, **kwargs):
        return render(request, 'job/resume-create.html', context={'title': title})

class SentView1(View):
    def get(self, request,pk):
        return render(request, 'job/sent.html', context={'title': title})

class SentView(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'job/sent.html'
    extra_context = {'title': title, }