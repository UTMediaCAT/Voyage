# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0021_sourcesitealias_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sourcesitealias',
            options={'verbose_name': 'Alias', 'verbose_name_plural': 'Aliases'},
        ),
    ]
