# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 05:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20171126_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberapplication',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Adresse'),
        ),
    ]
