# Generated by Django 4.2.3 on 2023-07-26 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_charityuserprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charityuserprofile',
            name='id',
        ),
        migrations.AlterField(
            model_name='charityuserprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]