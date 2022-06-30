# Generated by Django 3.2.9 on 2022-04-11 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('school_id', models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='school name')),
                ('locations', models.CharField(max_length=100, verbose_name='school location')),
                ('gps_location', models.CharField(max_length=50, verbose_name='Ghana GPS')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='School Account')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=60, verbose_name='full Name')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('address', models.CharField(max_length=60, verbose_name='address')),
                ('gps_location', models.CharField(max_length=60, verbose_name='ghana gps')),
                ('school_class', models.CharField(max_length=60, verbose_name='Class')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='null', max_length=10, verbose_name='gender')),
                ('school', models.ForeignKey(max_length=60, on_delete=django.db.models.deletion.CASCADE, to='students_school.school', verbose_name='school')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
