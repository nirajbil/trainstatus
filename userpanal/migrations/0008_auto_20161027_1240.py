# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-27 07:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpanal', '0007_api_key'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='API_Key',
            new_name='API_Key_model',
        ),
        migrations.RenameField(
            model_name='api_key_model',
            old_name='RailwayAPI_APIKEY',
            new_name='RailwayAPI_APIKEY_model',
        ),
    ]
