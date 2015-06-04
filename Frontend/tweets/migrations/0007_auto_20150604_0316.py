# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0006_auto_20150529_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='followers',
        ),
        migrations.AlterField(
            model_name='source',
            name='domain',
            field=models.URLField(max_length=2000, verbose_name=b'Source Site'),
            preserve_default=True,
        ),
    ]
