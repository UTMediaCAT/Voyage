# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0016_auto_20151204_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referringsitecssselector',
            name='regex',
            field=models.CharField(help_text=b'Regular expression to further narrow down', max_length=1000, blank=True),
            preserve_default=True,
        ),
    ]
