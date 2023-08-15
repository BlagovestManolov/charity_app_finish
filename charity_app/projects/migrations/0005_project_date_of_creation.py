# Generated by Django 4.2.3 on 2023-08-07 13:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_volunteers'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='date_of_creation',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
