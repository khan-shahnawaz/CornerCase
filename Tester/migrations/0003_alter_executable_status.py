# Generated by Django 4.0.5 on 2022-06-16 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tester', '0002_remove_executable_newfiled_executable_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executable',
            name='status',
            field=models.CharField(max_length=20),
        ),
    ]