# Generated by Django 3.1 on 2020-10-01 21:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0004_auto_20200929_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)]),
        ),
    ]
