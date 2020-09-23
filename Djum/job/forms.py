from django import forms
from .models import Application

'''
    written_username = models.CharField(max_length=32, verbose_name="Имя")
    written_phone = models.CharField(max_length=32, verbose_name="Телефон")
    written_cover_letter = models.TextField(verbose_name="Сопроводительное письмо")
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)
'''


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter', 'vacancy', 'user']
        widgets = {
            'written_username': forms.TextInput(attrs={'class': 'form-control'}),
            'written_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'written_cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,}),

        }
