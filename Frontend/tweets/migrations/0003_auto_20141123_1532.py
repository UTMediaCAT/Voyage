# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_tweet_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='source',
            old_name='source',
            new_name='url',
        ),
        migrations.AddField(
            model_name='source',
            name='url_origin',
            field=models.URLField(default='www.default.site'),
            preserve_default=False,
        ),
    ]
