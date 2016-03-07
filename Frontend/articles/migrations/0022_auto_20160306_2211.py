# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0021_migrate_article_urls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='url',
        ),
        migrations.AlterField(
            model_name='article',
            name='text_hash',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
