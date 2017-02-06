# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0005_furnacework'),
    ]

    operations = [
        migrations.AddField(
            model_name='furnacework',
            name='tempstatus',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]