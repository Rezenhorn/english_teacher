# Generated by Django 3.2.16 on 2023-01-23 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(help_text='dd.mm.yyyy', verbose_name='Date of birth'),
        ),
    ]