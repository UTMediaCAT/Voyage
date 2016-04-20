# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0020_auto_20160218_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcesitealias',
            name='name',
            field=models.CharField(default=b'', help_text=b'Your favorable name of this site.', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
