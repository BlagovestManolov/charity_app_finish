# Generated by Django 4.2.3 on 2023-07-30 13:12

import charity_app.projects.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(8), charity_app.projects.validators.project_name_validator])),
                ('project_description', models.TextField()),
                ('project_type', models.CharField(choices=[('LFV', 'Looking_For_Volunteers'), ('SFA', 'Seeking_Financial_Aid'), ('SMA', 'Seeking_Material_Aid')], max_length=3)),
                ('is_active', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
