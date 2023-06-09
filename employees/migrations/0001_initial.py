# Generated by Django 4.1.6 on 2023-04-11 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('departments', '0001_initial'),
        ('salaries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=45)),
                ('lastName', models.CharField(max_length=45)),
                ('phone', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45)),
                ('birthday', models.DateField()),
                ('address', models.CharField(max_length=500)),
                ('gender', models.BooleanField()),
                ('phoneNumber', models.CharField(max_length=45)),
                ('image', models.FileField(upload_to='')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='departments.department')),
                ('salary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='salaries.level_salary')),
            ],
            options={
                'db_table': 'employees',
            },
        ),
    ]
