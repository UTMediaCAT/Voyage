# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0010_auto_20150709_0316'),
    ]

    operations = [
        migrations.AddField(
            model_name='referringsite',
            name='check',
            field=models.BooleanField(default=True, verbose_name=b'Check Newspaper'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referringsite',
            name='mode',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'', verbose_name=b'Crawler', choices=[(0, b'Newspaper'), (1, b'Plan B'), (2, b'Both')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referringsite',
            name='url',
            field=models.URLField(help_text=b'Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://cnn.com)', unique=True, max_length=2000),
            preserve_default=True,
        ),
    ]
