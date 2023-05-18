# Generated by Django 4.1.6 on 2023-04-11 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=45)),
                ('phoneNumber', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'departments',
            },
        ),
    ]
