from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Specialty, Company, Vacancy, UserResume
from .forms import ApplicationForm, UserRegForm, UserAutForm, CompanyForm, VacancyForm, ResumeForm


class MainView(ListView):
    model = Specialty
    template_name = 'job/index.html'
    context_object_name = 'main_specialty'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['company'] = Company.objects.all()
        return context


# – Вакансии по специализации
class ListVacSpecialtiesView(ListView):
    template_name = 'job/vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 8

    def get_queryset(self):
        return Vacancy.objects.filter(specialty__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_specialty'] = Specialty.objects.get(slug=self.kwargs['slug'])
        context['number_vacancies'] = Vacancy.objects.filter(specialty__slug=self.kwargs['slug']).count()
        return context


# – Все вакансии списком
class ListVacanciesView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'job/vacancies.html'
    extra_context = {'number_vacancies': Vacancy.objects.count()}
    paginate_by = 8


# – Одна вакансия
class OneVacancyView(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'job/vacancy.html'


# – Карточка компании
class CardCompanyView(ListView):
    template_name = 'job/vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 8

    def get_queryset(self):
        return Vacancy.objects.filter(company__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_company'] = Company.objects.get(pk=self.kwargs['pk'])
        context['number_vacancies'] = Vacancy.objects.filter(company__pk=self.kwargs['pk']).count()
        return context


class CompaniesView(ListView):
    model = Company
    template_name = 'job/companies.html'
    context_object_name = 'companies'
    extra_context = {'number_companies': Company.objects.count()}
    paginate_by = 8


# ----------------------- 4 week --------------------
class CreateApplicationView(View):

    def get(self, request, pk):
        form = ApplicationForm()
        form.fields['vacancy'].initial = Vacancy.objects.get(pk=pk)
        form.fields['user'].initial = User.objects.get(pk=request.user.pk)
        return render(request, 'job/vacancy.html', context={
            'form': form,
            'vacancy': Vacancy.objects.get(pk=pk),
            'flag_application': 1,
        })

    def post(self, request, pk):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sent', pk)
        return render(request, 'job/vacancy.html', context={'form': form, })


# ------------------- регистрация и вход -------------------
class MySignupView(CreateView):
    form_class = UserRegForm
    success_url = 'login'
    template_name = 'signup.html'


class MyLogin(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main')
        form = UserAutForm()
        return render(request, 'login.html', {'form': form, })

    def post(self, request):
        form = UserAutForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
        return render(request, 'login.html', context={'form': form, })


# ----------------------- добавление и редактирование компании ----------------------------
class AddCompanyView(View):

    def get(self, request):
        form = CompanyForm()
        form.fields['owner'].initial = request.user
        return render(request, 'job/company-edit.html', context={'form': form, })

    def post(self, request):
        form = CompanyForm(request.POST)
        if form.is_valid():
            new_company = form.save()
            return redirect(new_company)
        return render(request, 'job/company-edit.html', context={'form': form, })


class UpdateCompanyView(UpdateView):
    """   редактирование компании    """
    model = Company
    # context_object_name = 'company'
    form_class = CompanyForm
    template_name = 'job/company-upd.html'


class MyVacanciesView(ListView):
    """ лист вакансий компаний аутифиц. пользователя с компанией """
    template_name = 'job/vacancy-list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(company__owner=self.request.user)


# ----------------------- user profile ----------------------------
class UserProfileView(DetailView):
    """ окно при нажатии на "компания" в выпадающем меню зарег пользователя,
    у которого нет компании (ссылка на допввление компании) """
    model = User
    template_name = 'job/user_prof.html'


class DemoCompView(View):
    """ окно при нажатии на "компания" в выпадающем меню зарег пользователя,
    у которого нет компании (ссылка на допввление компании) """
    def get(self, request, *args, **kwargs):
        return render(request, 'job/my_demo_company.html')


# ----------------------- добавление и редактирование вакансии ----------------------------
class AddVacancyView(View):

    def get(self, request):
        form = VacancyForm()
        # оставляет селект с 1-пунктом (без initial по умолчанию выбирается: ---------):
        form.fields['company'].queryset = Company.objects.filter(owner__pk=request.user.pk)
        # делает этот пункт выбранным (без queryset остается возможность выбора из всего списка)
        form.fields['company'].initial = Company.objects.get(owner__pk=request.user.pk)
        # form = UpdVacForm(initial={'company': Company.objects.get(owner__pk=request.user.pk)})
        return render(request, 'job/vacancy-add.html', context={'form': form, })

    def post(self, request):
        form = VacancyForm(request.POST)
        if form.is_valid():
            new_vacancy = form.save()
            return redirect(new_vacancy)
        return render(request, 'job/vacancy-add.html', context={'form': form, })


class UpdateVacancyView(UpdateView):
    """ правка вакансии """
    model = Vacancy
    form_class = VacancyForm
    template_name = 'job/vacancy-upd.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_vacancy'] = Vacancy.objects.get(pk=self.kwargs['pk'])
        return context


# ----------------------- Поиск ----------------------------
class SearcherView(ListView):
    context_object_name = 'vacancies'
    template_name = 'job/searcher.html'

    def get_queryset(self):
        return Vacancy.objects.filter(
            Q(title__icontains=self.request.GET.get('s')) |
            Q(description__icontains=self.request.GET.get('s')) |
            Q(skills__contains=self.request.GET.get('s'))
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_search'] = self.request.GET.get('s')
        return context


# ----------------------- добавление и редактирование резюме ----------------------------
class AddUserResumeView(View):
    def get(self, request):
        form = ResumeForm()
        form.fields['user'].initial = request.user
        return render(request, 'job/resume-edit.html', context={'form': form, })

    def post(self, request):
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.pk)
        return render(request, 'job/resume-edit.html', context={'form': form, })


class UpdUserResumeView(View):
    def get(self, request, pk):
        resume = UserResume.objects.get(pk=pk)
        form = ResumeForm(instance=resume)
        return render(request, 'job/resume-edit.html', context={'form': form, })

    def post(self, request, pk):
        resume = UserResume.objects.get(pk=pk)
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.pk)
        return render(request, 'job/resume-edit.html', context={'form': form, })


class DemoResumeView(View):
    """ окно при нажатии на "компания" в выпадающем меню зарег пользователя,
    у которого нет компании (ссылка на допввление компании) """

    def get(self, request):
        return render(request, 'job/resume-create.html')


class SentView(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'job/sent.html'


class About(View):
    def get(self, request):
        return render(request, 'job/about.html')
