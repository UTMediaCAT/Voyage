# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0002_auto_20141110_2322'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fsite',
            options={'verbose_name': 'Foreign Site'},
        ),
        migrations.AlterModelOptions(
            name='msite',
            options={'verbose_name': 'Monitoring Site'},
        ),
    ]
