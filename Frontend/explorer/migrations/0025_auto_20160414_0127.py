# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0024_auto_20160413_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keywordalias',
            name='primary',
        ),
        migrations.DeleteModel(
            name='KeywordAlias',
        ),
    ]
