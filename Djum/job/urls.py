"""Djum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LogoutView
from django.urls import path
from job.views import MainView, ListVacancies, CardCompany, ListVacSpecialties, Companies, OneVacancy, \
    CreateApplication, MySignupView, my_login, EditCompany, MyVacancies, UpdateComp, AddCompany, UserProf, \
    DemoComp, DemoSummary, AddVacancy, UpdateVacancy, Searcher, AddSummary, UpdSummary

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', ListVacancies.as_view(), name='vacancies'),
    path('company/', Companies.as_view(), name='companies'),
    path('company/<int:pk>', CardCompany.as_view(), name='company'),
    path('vacancies/cat/<str:slug>', ListVacSpecialties.as_view(), name='specialties'),
    path('vacancies/<int:pk>', OneVacancy.as_view(), name='vacancy'),
    path('vacancies/<int:pk>/send/', CreateApplication.as_view(), name='application'),
    path('addmycompany/', AddCompany.as_view(), name='addmycompany'),
    path('mycompany/', EditCompany.as_view(), name='mycompany'),
    path('mycompany/<int:pk>', UpdateComp.as_view(), name='update_comp'),
    path('mycompany/vacancies/', MyVacancies.as_view(), name='myvacancies'),
    path('profile/<int:pk>', UserProf.as_view(), name='profile'),
    path('demo/', DemoComp.as_view(), name='demo'),
    path('demos/', DemoSummary.as_view(), name='demos'),
    path('mycompany/vacancies/add/', AddVacancy.as_view(), name='add_vac'),
    path('mycompany/vacancies/<int:pk>', UpdateVacancy.as_view(), name='update_vac'),
    path('searcher/', Searcher.as_view(), name='searcher'),
    path('addsummary/<int:pk>', AddSummary.as_view(), name='addsummary'),
    path('updsummary/<int:pk>', UpdSummary.as_view(), name='updsummary'),

]

urlpatterns += [
    path('login', my_login, name='login'),
    # path('login', MyLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', MySignupView.as_view(), name='signup'),
]
