# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banquet', '0008_auto_20181007_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='banquet',
            name='caption_dietary_restrictions',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Caption for dietary restrictions'),
        ),
        migrations.AddField(
            model_name='banquet',
            name='caption_phone_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Caption for the phone number field'),
        ),
        migrations.AddField(
            model_name='banquet',
            name='dress_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
