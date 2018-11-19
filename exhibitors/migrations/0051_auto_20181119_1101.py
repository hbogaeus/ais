# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 11:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0050_auto_20181111_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exhibitor',
            options={'default_permissions': [], 'ordering': ['company__name'], 'permissions': [('base', 'View the Exhibitors tab'), ('view_all', 'Always view all exhibitors'), ('create', 'Create new exhibitors'), ('modify_contact_persons', 'Modify contact persons'), ('modify_transport', 'Modify transport details'), ('modify_check_in', 'Modify check in'), ('modify_details', 'Modify details')]},
        ),
    ]
