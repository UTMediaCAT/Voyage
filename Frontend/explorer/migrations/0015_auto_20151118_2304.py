# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0014_auto_20151118_2254'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referringsitecssselector',
            options={'verbose_name': 'CSS Selector'},
        ),
        migrations.AlterModelOptions(
            name='referringsitefilter',
            options={'verbose_name': 'Filter'},
        ),
    ]
