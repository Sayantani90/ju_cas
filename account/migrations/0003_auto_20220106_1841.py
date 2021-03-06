# Generated by Django 2.2.15 on 2022-01-06 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20220106_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='dob',
            field=models.DateField(auto_now=True, verbose_name='DOB'),
        ),
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'M'), ('Female', 'F')], max_length=6, null=True, verbose_name='Gender(M/F)'),
        ),
    ]
