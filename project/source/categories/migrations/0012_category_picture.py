# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-22 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0011_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='picture',
            field=models.ImageField(blank=True, height_field=500, upload_to=b'', verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430', width_field=800),
        ),
    ]