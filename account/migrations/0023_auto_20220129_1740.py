# Generated by Django 2.2.15 on 2022-01-29 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_auto_20220129_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='addr_perm',
            field=models.SlugField(blank=True, max_length=300, null=True, verbose_name='Address for permanent'),
        ),
        migrations.AlterField(
            model_name='account',
            name='dt_eligibility',
            field=models.DateField(null=True, verbose_name='Date of promo elig'),
        ),
        migrations.AlterField(
            model_name='account',
            name='dt_last_promo',
            field=models.DateField(null=True, verbose_name='Date of last promotion'),
        ),
    ]
