# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 11:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_memberapplication_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberapplication',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memberapplication',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
