# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0002_auto_20170125_2237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Furnace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work', models.BooleanField(default=False)),
            ],
        ),
    ]
