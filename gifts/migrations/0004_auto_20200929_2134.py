# Generated by Django 3.1 on 2020-09-29 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0003_auto_20200929_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
