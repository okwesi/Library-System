# Generated by Django 3.2.9 on 2022-05-16 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_school', '0010_student_borrowed'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='borrowed',
            field=models.BooleanField(default=False),
        ),
    ]
