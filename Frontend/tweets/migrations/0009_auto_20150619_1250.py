# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0008_auto_20150619_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcesite',
            name='matched',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sourcetwitter',
            name='matched',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
