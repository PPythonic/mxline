# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default='', verbose_name='视频链接'),
        ),
    ]
