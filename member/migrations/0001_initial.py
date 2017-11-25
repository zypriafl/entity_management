# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birthday', models.DateField()),
                ('phone_number', models.CharField(max_length=50)),
                ('street_name', models.CharField(max_length=100)),
                ('street_number', models.CharField(max_length=25)),
                ('postal_code', models.CharField(max_length=25)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('membership_type', models.CharField(choices=[('active', 'Aktiv'), ('active_cheerleading', 'Aktiv - Cheerleading'), ('support', 'F\xf6rdermitglied')], max_length=50)),
                ('position_type', models.CharField(choices=[('board_1', '1. Vorsitzender'), ('board_2', '2. Vorsitzender'), ('board_3', 'Finanzvorstand')], max_length=50)),
            ],
        ),
    ]
