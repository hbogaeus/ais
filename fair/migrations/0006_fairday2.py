# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-11 12:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0005_fairday_lunchticket_lunchticketscan_lunchtickettime'),
    ]

    operations = [
        migrations.CreateModel(
            name='FairDay2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(max_length=255)),
                ('fair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fair.Fair')),
            ],
            options={
                'ordering': ['fair', 'date'],
                'default_permissions': [],
            },
        ),
    ]