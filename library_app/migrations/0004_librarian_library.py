# Generated by Django 3.2.9 on 2022-04-13 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0003_remove_librarian_library'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarian',
            name='library',
            field=models.ForeignKey(default='fddd3082-3556-4732-a77b-8767904d52fb', on_delete=django.db.models.deletion.CASCADE, to='library_app.library'),
            preserve_default=False,
        ),
    ]
