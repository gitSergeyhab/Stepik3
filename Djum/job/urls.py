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
    CreateApplication, MySignupView, my_login

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', ListVacancies.as_view(), name='vacancies'),
    path('company/', Companies.as_view(), name='companies'),
    path('company/<int:pk>', CardCompany.as_view(), name='company'),
    path('vacancies/cat/<str:slug>', ListVacSpecialties.as_view(), name='specialties'),
    path('vacancies/<int:pk>', OneVacancy.as_view(), name='vacancy'),
    path('vacancies/<int:pk>/send/', CreateApplication.as_view(), name='application'),
    # path('mycompany/', Mycompany.as_view(),  name='mycompany'),
]


urlpatterns += [
    path('login', my_login, name='login'),
    # path('login', MyLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', MySignupView.as_view(), name='signup'),
]


