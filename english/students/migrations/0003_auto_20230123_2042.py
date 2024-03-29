# Generated by Django 3.2.16 on 2023-01-23 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='progress',
            options={'ordering': ('id',), 'verbose_name_plural': 'Progress'},
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='example',
            field=models.CharField(blank=True, help_text='A sentence with the word', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dictionary', to='users.user', verbose_name='Student'),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='translation',
            field=models.CharField(max_length=150),
        ),
    ]
