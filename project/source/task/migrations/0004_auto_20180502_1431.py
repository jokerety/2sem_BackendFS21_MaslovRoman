# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-02 14:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_task_prescription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='is_archieve',
            new_name='is_finished',
        ),
    ]
