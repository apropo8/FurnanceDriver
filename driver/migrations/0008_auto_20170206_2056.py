# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0007_setusertemp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='furnacework',
            name='temp',
            field=models.FloatField(max_length=200),
        ),
    ]
