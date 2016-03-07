# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0019_auto_20160218_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referringsite',
            name='name',
            field=models.CharField(help_text=b'Your favorable name of this site.\nMaximum 200 characters', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sourcesite',
            name='name',
            field=models.CharField(help_text=b'Your favorable name of this site.', unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
