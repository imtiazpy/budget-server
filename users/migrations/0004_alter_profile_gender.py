# Generated by Django 4.0.4 on 2022-06-03 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.IntegerField(choices=[('Male', 1), ('Female', 2), ('Others', 3)]),
        ),
    ]