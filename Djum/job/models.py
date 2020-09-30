from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from random import choice, shuffle

from job.data import jobs, skillist, companies, cities, specialties, level


class EducationChoices(Enum):
    missing = 'Отсутствует'
    secondary = 'Среднее'
    vocational = 'Средне-специальное'
    incomplete_higher = 'Неполное высшее'
    higher = 'Высшее'


class GradeChoices(Enum):
    intern = 'intern'
    junior = 'junior'
    middle = 'middle'
    senior = 'senior'
    lead = 'lead'


class SpecialtyChoices(Enum):
    frontend = 'Фронтенд'
    backend = 'Бэкенд'
    gamedev = 'Геймдев'
    devops = 'Девопс'
    design = 'Дизайн'
    products = 'Продукты'
    management = 'Менеджмент'
    testing = 'Тестирование'


class WorkStatusChoices(Enum):
    not_in_search = 'Не ищу работу'
    consideration = 'Рассматриваю предложения'
    in_search = 'Ищу работу'


class Company(models.Model):
    name = models.CharField(max_length=32, verbose_name="Компания", unique=True)
    location = models.CharField(max_length=32, verbose_name="Город", blank=True)
    logo = models.ImageField(verbose_name="Логотип", upload_to="logs/%Y/%m/%d/", blank=True)
    description = models.TextField(verbose_name="Информация о компании", blank=True)
    employee_count = models.IntegerField(verbose_name="Количество сотрудников", null=True, blank=True)
    owner = models.OneToOneField(User, related_name="company", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('company', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class Specialty(models.Model):
    code = models.CharField(max_length=32, verbose_name="Код", unique=True)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=32, verbose_name="Специализация")
    picture = models.ImageField(verbose_name="Картинка", upload_to="pics/%Y/%m/%d/", blank=True)

    def get_absolute_url(self):
        return reverse('specialties', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"


class Vacancy(models.Model):
    title = models.CharField(max_length=64, verbose_name="Профессия")
    specialty = models.ForeignKey(Specialty, related_name="vacancies", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=models.CASCADE)
    skills = models.TextField(verbose_name="Навыки")
    level = models.CharField(max_length=16, verbose_name="Уровень")
    description = models.TextField(verbose_name="Описание", blank=True)
    salary_min = models.IntegerField(verbose_name="Зарплата от")
    salary_max = models.IntegerField(verbose_name="Зарплата до")
    published_at = models.DateField(verbose_name="Опубликовано", auto_now_add=True)

    # def get_absolute_url(self):
    #     return reverse('vacancies', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('application', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-published_at']


def skill_maker(x):
    shuffle(skillist)
    xx = list(range(x - 1, x + 1))
    return ' • '.join(skillist[:choice(xx)])


def usermakerX(x):
    # return 'username' + str(x), 'first_name' + str(x), 'last_name' + str(x)
    return 'username' + str(x), 'email' + str(x) + '@mail.fake', 'pass' + str(x) + 'word'


def random_database():
    # число юзеров, компаний, специальностей, вакансий = ....
    nun_users, num_coms, num_sps, num_vacs = 40, 8, 8, 40
    somelist = list(range(40))
    shuffle(somelist)

    if User.objects.count() < nun_users:
        for i in range(nun_users):
            q, w, e = usermakerX(i)
            User.objects.create_user(username=q, email=w, password=e)

    c = 0
    for com in companies:
        c += 1
        if Company.objects.count() < num_coms:
            Company.objects.create(
                name=com['title'], location=choice(cities),
                employee_count=choice(list(range(1, 500))),
                owner=User.objects.get(username=str('username' + str(somelist[c])))
            )

    for sp in specialties:
        if Specialty.objects.count() < num_sps:
            Specialty.objects.create(code=sp['code'], slug=sp['code'], title=sp['title'])

    for j in jobs:
        if Vacancy.objects.count() < num_vacs:
            Vacancy.objects.create(
                title=j['title'],
                specialty=Specialty.objects.filter(code=j['cat'])[0],
                company=Company.objects.filter(name=j['company'])[0],
                skills=skill_maker(6), level=choice(level), description=j['desc'],
                salary_min=j['salary_from'], salary_max=j['salary_to']
            )


##                                                  --- week 4 ---


class Application(models.Model):
    written_username = models.CharField(max_length=32, verbose_name="Вас зовут")
    written_phone = models.CharField(max_length=32, verbose_name="Ваш телефон")
    written_cover_letter = models.TextField(verbose_name="Сопроводительное письмо")
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('application', kwargs={'pk': self.pk})

    def __str__(self):
        return self.written_username

    class Meta:
        ordering = ['written_username']
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"

# ------------------ резюме ------------------
# этот вариант не работает - выдает
# class UserSummary(models.Model):
#     user = models.OneToOneField(User, related_name="summary", on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=32)
#     last_name = models.CharField(max_length=32)
#     readiness = models.CharField(
#           max_length=32,
#           choices=[(tag, tag.value) for tag in WorkStatusChoices])
#     salary = models.PositiveIntegerField()
#     specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
#     level = models.CharField(
#           max_length=32,
#           choices=[(tag, tag.value) for tag in GradeChoices])
#     education = models.CharField(
#           max_length=32,
#           choices=[(tag, tag.value) for tag in EducationChoices])
#     experience = models.TextField()
#     portfolio = models.CharField(max_length=32)
#
#     def get_absolute_url(self):
#         return reverse('usersummary', kwargs={'pk': self.user.pk})
#
#     def __str__(self):
#         return self.first_name, self.last_name


class UserSummary(models.Model):
    EducationChoices = {
        ('missing', 'Отсутствует'),
        ('secondary', 'Среднее'),
        ('vocational', 'Средне-специальное'),
        ('incomplete_higher', 'Неполное высшее'),
        ('higher', 'Высшее'),
    }

    GradeChoices = {
        ('intern', 'intern'),
        ('junior', 'junior'),
        ('middle', 'middle'),
        ('senior', 'senior'),
        ('lead', 'lead'),
    }
    WorkStatusChoices = {
        ('not_in_search', 'Не ищу работу'),
        ('consideration', 'Рассматриваю предложения'),
        ('in_search', 'Ищу работу'),
    }

    user = models.OneToOneField(User, related_name="summary", on_delete=models.CASCADE, verbose_name="Юзер")
    first_name = models.CharField(max_length=32, verbose_name="Имя")
    last_name = models.CharField(max_length=32, verbose_name="Фамилия")
    readiness = models.CharField(
        max_length=32,
        choices=WorkStatusChoices, verbose_name="Готовность")
    salary = models.PositiveIntegerField(verbose_name="Хочу")
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name="Специализация")
    level = models.CharField(
        max_length=32,
        choices=GradeChoices, verbose_name="Крутость")
    education = models.CharField(
        max_length=32,
        choices=EducationChoices, verbose_name="Образование")
    experience = models.TextField( verbose_name="Опыт")
    portfolio = models.CharField(max_length=32)

    def get_absolute_url(self):
        return reverse('updsummary', kwargs={'pk': self.pk})

    def __str__(self):
        return ' '.join((self.first_name, self.last_name))

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"



# раскомментировать при создании базы данных:
# random_database()
