# Generated by Django 2.2.15 on 2022-01-07 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20220107_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='dob',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date of birth'),
        ),
    ]