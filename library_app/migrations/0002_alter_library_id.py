# Generated by Django 3.2.9 on 2022-04-09 09:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='id',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='library id'),
        ),
    ]
