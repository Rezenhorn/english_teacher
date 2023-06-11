from django.conf import settings
from django.db import migrations


def copy_data(apps, schema_editor):
    if not apps.is_installed('students'):
        return

    StudentDictionary = apps.get_model('students', 'Dictionary')
    NewDictionary = apps.get_model('dictionary', 'Dictionary')

    old_objects = StudentDictionary.objects.all()
    for obj in old_objects:
        new_obj = NewDictionary()
        new_obj.word = obj.word
        new_obj.translation = obj.translation
        new_obj.transcription = obj.transcription
        new_obj.student = obj.student
        new_obj.date = obj.date
        new_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_data),
    ]
