# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 22:23


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20171126_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_since',
            field=models.DateField(verbose_name='Mitlied seit'),
        ),
    ]
