from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from random import choice, shuffle

from job.data import jobs, skillist, companies, cities, specialties, level


class Company(models.Model):
    name = models.CharField(max_length=32, verbose_name="Компания", unique=True)
    location = models.CharField(max_length=32, verbose_name="Город", blank=True)
    logo = models.ImageField(verbose_name="Логотип", upload_to="logs/%Y/%m/%d/", blank=True)
    description = models.TextField(verbose_name="Информация о компании", blank=True)
    employee_count = models.IntegerField(verbose_name="Количество сотрудников", null=True, blank=True)
    owner = models.ForeignKey(User, related_name="company", on_delete=models.CASCADE)

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


def usermakerX(x):
    # return 'username' + str(x), 'first_name' + str(x), 'last_name' + str(x)
    return 'username' + str(x), 'email' + str(x) + '@mail.fake', 'pass' + str(x) + 'word'


def random_database():
    # число юзеров, компаний, специальностей, вакансий = ....
    nun_users, num_coms, num_sps, num_vacs = 40, 8, 8, 40

    if User.objects.count() < nun_users:
        for i in range(nun_users):
            q, w, e = usermakerX(i)
            User.objects.create_user(username=q, email=w, password=e)

    for com in companies:
        if Company.objects.count() < num_coms:
            Company.objects.create(
                name=com['title'], location=choice(cities),
                employee_count=choice(list(range(1, 500))),
                owner=User.objects.get(username=str('username' + str(choice(list(range(nun_users))))))
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

# раскомментировать при создании базы данных:
random_database()
