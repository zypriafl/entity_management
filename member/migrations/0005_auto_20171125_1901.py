# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 18:01


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20171125_1257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name': 'Mitglied', 'verbose_name_plural': 'Mitglieder'},
        ),
        migrations.AlterField(
            model_name='member',
            name='application_form',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.MemberApplication', verbose_name='Mitgliedsantrag'),
        ),
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.DateField(verbose_name='Geburtsdatum'),
        ),
        migrations.AlterField(
            model_name='member',
            name='city',
            field=models.CharField(max_length=100, verbose_name='Stadt'),
        ),
        migrations.AlterField(
            model_name='member',
            name='country',
            field=models.CharField(max_length=100, verbose_name='Land'),
        ),
        migrations.AlterField(
            model_name='member',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='erstellt am'),
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email Adresse'),
        ),
        migrations.AlterField(
            model_name='member',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Vorname'),
        ),
        migrations.AlterField(
            model_name='member',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Nachname'),
        ),
        migrations.AlterField(
            model_name='member',
            name='membership_type',
            field=models.CharField(choices=[('active', 'Aktiv'), ('active_cheerleading', 'Aktiv - Cheerleading'), ('support', 'F\xf6rdermitglied')], max_length=50, verbose_name='Art der Mitgliedschaft'),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone_number',
            field=models.CharField(max_length=50, verbose_name='Telefonnummer'),
        ),
        migrations.AlterField(
            model_name='member',
            name='position_type',
            field=models.CharField(choices=[('board_1', '1. Vorsitzender'), ('board_2', '2. Vorsitzender'), ('board_3', 'Finanzvorstand')], max_length=50, verbose_name='Position im Verein'),
        ),
        migrations.AlterField(
            model_name='member',
            name='postal_code',
            field=models.CharField(max_length=25, verbose_name='Postleitzahl'),
        ),
        migrations.AlterField(
            model_name='member',
            name='street_name',
            field=models.CharField(max_length=100, verbose_name='Stra\xdfe'),
        ),
        migrations.AlterField(
            model_name='member',
            name='street_number',
            field=models.CharField(max_length=25, verbose_name='Hausnummer'),
        ),
        migrations.AlterField(
            model_name='member',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='ge\xe4ndert am'),
        ),
    ]
