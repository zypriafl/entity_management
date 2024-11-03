# Generated by Django 5.1.2 on 2024-11-03 20:40

import localflavor.generic.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_auto_20171226_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberapplication',
            name='gender',
            field=models.CharField(choices=[('female', 'Frau'), ('male', 'Mann'), ('divers', 'Divers')], max_length=50, null=True, verbose_name='Geschlecht'),
        ),
        migrations.AlterField(
            model_name='memberapplication',
            name='iban',
            field=localflavor.generic.models.IBANField(include_countries=('AD', 'AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GB', 'GI', 'GR', 'HR', 'HU', 'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MC', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'SM', 'VA'), max_length=34, null=True, use_nordea_extensions=False, verbose_name='Deine IBAN'),
        ),
    ]