# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 22:21
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_auto_20171126_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='member_since',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Mitlied seit'),
            preserve_default=False,
        ),
    ]
