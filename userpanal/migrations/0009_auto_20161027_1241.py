# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-27 07:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpanal', '0008_auto_20161027_1240'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='API_Key_model',
            new_name='API_Key',
        ),
        migrations.RenameField(
            model_name='api_key',
            old_name='RailwayAPI_APIKEY_model',
            new_name='RailwayAPI_APIKEY',
        ),
    ]