# Generated by Django 4.2.4 on 2023-08-14 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_charityuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charityuser',
            name='user_type',
            field=models.CharField(choices=[('U', 'User'), ('O', 'Organization')], default='User', max_length=12),
        ),
    ]
