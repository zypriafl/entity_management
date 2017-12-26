# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 19:43
from __future__ import unicode_literals

from django.db import migrations, models
import localflavor.generic.models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0012_auto_20171219_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='bic',
            field=localflavor.generic.models.BICField(blank=True, max_length=11, null=True, verbose_name='BIC'),
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-Mail Adresse'),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban',
            field=localflavor.generic.models.IBANField(blank=True, include_countries=('AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GB', 'GI', 'GR', 'HR', 'HU', 'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MC', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'SM'), max_length=34, null=True, use_nordea_extensions=False, verbose_name='IBAN'),
        ),
    ]
