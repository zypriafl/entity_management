# Generated by Django 4.1.7 on 2023-03-09 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0020_member_paid_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='paid_2023',
            field=models.BooleanField(default=False, null=True, verbose_name='bezahlt 2023?'),
        ),
    ]