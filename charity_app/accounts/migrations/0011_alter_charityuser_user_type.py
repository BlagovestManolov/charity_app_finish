# Generated by Django 4.2.3 on 2023-08-09 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_organizationuserprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charityuser',
            name='user_type',
            field=models.CharField(choices=[('U', 'User'), ('O', 'Organization')], default='U', max_length=1),
        ),
    ]
