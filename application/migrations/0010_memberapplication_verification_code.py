# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 05:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_auto_20171127_0632'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberapplication',
            name='verification_code',
            field=models.CharField(default='temp', editable=False, max_length=64),
            preserve_default=False,
        ),
    ]