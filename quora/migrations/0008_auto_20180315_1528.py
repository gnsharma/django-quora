# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-15 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0007_auto_20180313_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='questions',
        ),
        migrations.AddField(
            model_name='question',
            name='topics',
            field=models.ManyToManyField(blank=True, to='quora.Topic'),
        ),
    ]
