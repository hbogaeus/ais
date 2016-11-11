# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-09 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import lib.image


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('map_image', models.ImageField(upload_to=lib.image.UploadToDir('building'))),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=80)),
                ('floor', models.PositiveSmallIntegerField(default=0)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Building')),
            ],
        ),
        migrations.RemoveField(
            model_name='location',
            name='address',
        ),
        migrations.RemoveField(
            model_name='location',
            name='building',
        ),
        migrations.RemoveField(
            model_name='location',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='location',
            name='description',
        ),
        migrations.RemoveField(
            model_name='location',
            name='floor',
        ),
        migrations.RemoveField(
            model_name='location',
            name='name',
        ),
        migrations.AddField(
            model_name='location',
            name='x_pos',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='location',
            name='y_pos',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='location',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Room'),
        ),
    ]