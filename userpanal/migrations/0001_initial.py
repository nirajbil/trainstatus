# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-26 06:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PNRNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnr_no', models.CharField(max_length=20)),
                ('notification_type', models.CharField(max_length=10)),
                ('notification_type_value', models.CharField(max_length=50)),
                ('notification_frequency', models.CharField(max_length=20)),
                ('notification_frequency_value', models.CharField(max_length=10)),
                ('next_schedule_time', models.DateTimeField()),
                ('notify_on_status_change', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PNRStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnr_no', models.CharField(max_length=20)),
                ('status', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='RecentPNR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RecentPnrNo', models.CharField(max_length=20)),
                ('Srcdest', models.CharField(max_length=20)),
                ('DateOfJourney', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_me', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]
