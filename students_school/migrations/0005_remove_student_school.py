# Generated by Django 3.2.9 on 2022-04-13 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students_school', '0004_alter_school_school_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='school',
        ),
    ]
