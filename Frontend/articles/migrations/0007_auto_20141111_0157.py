# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20141110_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_added',
            field=models.DateTimeField(null=True, verbose_name=b'Date Added', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='date_published',
            field=models.DateTimeField(null=True, verbose_name=b'Date Published', blank=True),
            preserve_default=True,
        ),
    ]
