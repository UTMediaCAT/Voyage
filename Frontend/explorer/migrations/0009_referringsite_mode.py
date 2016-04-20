# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0008_auto_20150619_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='referringsite',
            name='mode',
            field=models.BooleanField(default=False, help_text=b'If you want to use Plan B instead of Newspaper, tick'),
            preserve_default=True,
        ),
    ]
