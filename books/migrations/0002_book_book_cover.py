# Generated by Django 3.2.9 on 2022-07-05 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_cover',
            field=models.ImageField(default='', upload_to='books/'),
            preserve_default=False,
        ),
    ]
