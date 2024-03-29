# Generated by Django 3.2.20 on 2023-07-31 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dictionary', '0003_rename_dictionary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='example',
            field=models.CharField(default='-', help_text='A sentence with the word', max_length=150),
        ),
        migrations.AlterField(
            model_name='word',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to=settings.AUTH_USER_MODEL, verbose_name='Student'),
        ),
    ]
