# Generated by Django 3.2.9 on 2022-08-14 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20220727_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('time_created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
