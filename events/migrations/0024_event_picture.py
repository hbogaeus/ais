# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-25 15:10
from __future__ import unicode_literals

from django.db import migrations, models
import lib.image


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20181019_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=lib.image.UploadToDirUUID('events', 'pictures')),
        ),
    ]