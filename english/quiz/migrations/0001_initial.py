# Generated by Django 3.2.20 on 2023-07-14 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dictionary', '0002_copy_old_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Quiz time')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
            options={
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answer', models.CharField(blank=True, max_length=255, verbose_name='Answer of student')),
                ('options', models.JSONField(default=list, help_text='Example: ["option1", "option2", "option3"]', verbose_name='Answer options')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dictionary.dictionary')),
            ],
        ),
    ]
