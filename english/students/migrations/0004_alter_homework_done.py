# Generated by Django 3.2.16 on 2022-10-22 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_homework_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='done',
            field=models.BooleanField(default=False, verbose_name='Done'),
        ),
    ]
