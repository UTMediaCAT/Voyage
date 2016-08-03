# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Frontend.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcesite',
            name='domain',
            field=Frontend.fields.URLProtocolField(max_length=2000, verbose_name=b'Source Site'),
            preserve_default=True,
        ),
    ]
