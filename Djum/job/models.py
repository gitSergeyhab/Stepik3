from django.db import models
from django.urls import reverse

from random import choice, shuffle

from job.data import jobs, skillist, companies, cities, specialties, level


class Company(models.Model):
    name = models.CharField(max_length=32, verbose_name="Компания")
    location = models.CharField(max_length=32, verbose_name="Город", blank=True)
    logo = models.ImageField(verbose_name="Логотип", upload_to="logs/%Y/%m/%d/", blank=True)
    description = models.TextField(verbose_name="Информация о компании", blank=True)
    employee_count = models.IntegerField(verbose_name="Количество сотрудников", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('company', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class Specialty(models.Model):
    code = models.CharField(max_length=32, verbose_name="Код")
    slug = models.SlugField()
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

    def get_absolute_url(self):
        return reverse('vacancies', kwargs={'pk': self.pk})

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


def random_database():
    for com in companies:
        if Company.objects.count() < 8:
            Company.objects.create(name=com['title'], location=choice(cities),
                                   employee_count=choice(list(range(1, 500))))
    for sp in specialties:
        if Specialty.objects.count() < 8:
            Specialty.objects.create(code=sp['code'], slug=sp['code'], title=sp['title'])
    for j in jobs:
        if Vacancy.objects.count() < 40:
            Vacancy.objects.create(title=j['title'],
                                   specialty=Specialty.objects.filter(code=j['cat'])[0],
                                   company=Company.objects.filter(name=j['company'])[0],
                                   skills=skill_maker(6), level=choice(level), description=j['desc'],
                                   salary_min=j['salary_from'], salary_max=j['salary_to'])

# раскомментировать при создании базы данных:
# random_database()
