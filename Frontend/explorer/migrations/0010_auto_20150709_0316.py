# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0009_referringsite_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referringsite',
            name='mode',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'If you want to use Plan B instead of Newspaper, tick', verbose_name=b'Crawler', choices=[(0, b'Newspaper'), (1, b'Plan B'), (2, b'Both')]),
            preserve_default=True,
        ),
    ]
