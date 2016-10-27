# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-26 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userpanal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pnrnotification',
            name='userprofile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userpanal.UserProfile'),
        ),
        migrations.AddField(
            model_name='pnrstatus',
            name='userprofile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userpanal.UserProfile'),
        ),
        migrations.AddField(
            model_name='recentpnr',
            name='userprofile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userpanal.UserProfile'),
        ),
    ]
