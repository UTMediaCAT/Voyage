# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20150619_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcesite',
            name='local',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sourcesite',
            name='matched',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sourcetwitter',
            name='matched',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
