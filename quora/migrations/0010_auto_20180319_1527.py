# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-19 09:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0009_auto_20180319_1135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answervotes',
            old_name='vote',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='questionvotes',
            old_name='vote',
            new_name='value',
        ),
    ]