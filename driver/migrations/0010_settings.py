# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0008_auto_20170206_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('savefurnacepower', models.CharField(max_length=200)),
                ('saveweatherpower', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
            ],
        ),
    ]
