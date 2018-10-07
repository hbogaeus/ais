# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-07 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_participant_signup_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='leader',
        ),
        migrations.AddField(
            model_name='teammember',
            name='leader',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='teammember',
            unique_together=set([('team', 'leader')]),
        ),
    ]