# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-12 10:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0004_auto_20180312_1230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='answerer',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='questioner',
            new_name='user',
        ),
    ]