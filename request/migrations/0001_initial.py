# Generated by Django 3.2.9 on 2022-05-14 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students_school', '0010_student_borrowed'),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(auto_now_add=True)),
                ('returned_date', models.DateField(blank=True, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('Pending Approval', 'Pending Approval'), ('Approved', 'Approved'), ('Delivered', 'Delivered'), ('Returned', 'Returned')], max_length=200)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students_school.school')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students_school.student')),
            ],
        ),
    ]
