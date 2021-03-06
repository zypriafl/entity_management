# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 22:19


from django.db import migrations, models

import application.models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_auto_20171126_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberapplication',
            name='wants_to_be_member',
            field=models.BooleanField(default=False, validators=[application.models.validate_true], verbose_name='Ich möchte zum nächstmöglichen Zeitpunkt Mitglied im Studylife München e.V werden. Um den Mitgliedsantrag abzuschicken klicke auf "Sichern".'),
        ),
    ]
