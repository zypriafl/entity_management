# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 11:59


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_auto_20171125_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberapplication',
            name='is_new',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
