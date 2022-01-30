# Generated by Django 2.2.15 on 2022-01-27 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20220126_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='Designation',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='to_dsg',
            field=models.CharField(blank=True, choices=[(None, 'Select Posts'), ('Stage 2', 'Assistant Prof. (Stage 2)'), ('Stage 3', 'Assistant Prof. (Stage 3)'), ('Stage 4', 'Associate Prof. (Stage 4)'), ('Stage 5', 'Professor (Stage 5)')], max_length=30, null=True, verbose_name='To stage/desgn.'),
        ),
        migrations.DeleteModel(
            name='Designation',
        ),
    ]
