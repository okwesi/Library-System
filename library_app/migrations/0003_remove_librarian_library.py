# Generated by Django 3.2.9 on 2022-04-13 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0002_alter_library_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='librarian',
            name='library',
        ),
    ]
