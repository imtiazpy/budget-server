# Generated by Django 4.0.4 on 2022-06-04 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], default=1, verbose_name='Gender'),
        ),
    ]