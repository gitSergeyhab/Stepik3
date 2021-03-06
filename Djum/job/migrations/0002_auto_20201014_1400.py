# Generated by Django 3.1.1 on 2020-10-14 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, upload_to='MEDIA_COMPANY_IMAGE_DIR', verbose_name='Логотип'),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='picture',
            field=models.ImageField(blank=True, upload_to='MEDIA_SPECIALITY_IMAGE_DIR', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='userresume',
            name='education',
            field=models.CharField(choices=[('Средне-специальное', 'Средне-специальное'), ('Неполное высшее', 'Неполное высшее'), ('Среднее', 'Среднее'), ('Отсутствует', 'Отсутствует'), ('Высшее', 'Высшее')], max_length=32, verbose_name='Образование'),
        ),
        migrations.AlterField(
            model_name='userresume',
            name='level',
            field=models.CharField(choices=[('middle', 'middle'), ('intern', 'intern'), ('senior', 'senior'), ('lead', 'lead'), ('junior', 'junior')], max_length=32, verbose_name='Крутость'),
        ),
        migrations.AlterField(
            model_name='userresume',
            name='readiness',
            field=models.CharField(choices=[('Рассматриваю предложения', 'Рассматриваю предложения'), ('Не ищу работу', 'Не ищу работу'), ('Ищу работу', 'Ищу работу')], max_length=32, verbose_name='Готовность'),
        ),
    ]
