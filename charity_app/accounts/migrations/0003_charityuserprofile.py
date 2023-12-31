# Generated by Django 4.2.3 on 2023-07-26 06:39

import charity_app.accounts.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_charityuser_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharityUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(3), charity_app.accounts.validators.name_validator])),
                ('last_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(3), charity_app.accounts.validators.name_validator])),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.MinLengthValidator(10), charity_app.accounts.validators.phone_number_validator])),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='user-photo/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
