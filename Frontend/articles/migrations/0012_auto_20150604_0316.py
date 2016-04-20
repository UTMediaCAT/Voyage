# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20150529_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='domain',
            field=models.URLField(max_length=2000, verbose_name=b'Referring Site'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='domain',
            field=models.URLField(max_length=2000, verbose_name=b'Source Site'),
            preserve_default=True,
        ),
    ]
