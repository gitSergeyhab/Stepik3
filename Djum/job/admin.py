from django.contrib import admin

# Register your models here.
from .models import Specialty, Company, Vacancy, Application



class VacancyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'level', 'specialty', 'company', 'salary_min', 'salary_max', 'published_at']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'specialty', 'company', 'published_at']
    list_filter = ['level', 'specialty', 'company']


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'code', 'slug']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('code',)}


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'employee_count']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'location', 'employee_count']


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['written_username', 'written_phone', 'vacancy', 'user']
    list_display_links = ['user']
    search_fields = ['written_username']
    list_filter = ['vacancy']



'''
    written_username = models.CharField(max_length=32, verbose_name="Имя")
    written_phone = models.CharField(max_length=32, verbose_name="Телефон")
    written_cover_letter = models.TextField(verbose_name="Сопроводительное письмо")
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)

'''

admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Application, ApplicationAdmin)
