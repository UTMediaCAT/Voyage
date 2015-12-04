# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_article_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcesite',
            name='anchor_text',
            field=models.CharField(default='', max_length=2000, verbose_name=b'Anchor Text'),
            preserve_default=False,
        ),
    ]
