# Generated by Django 4.0.5 on 2022-06-23 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tester', '0004_remove_test_passed_test_verdict'),
    ]

    operations = [
        migrations.AddField(
            model_name='programminglanguage',
            name='dockerImage',
            field=models.TextField(null=True),
        ),
    ]
