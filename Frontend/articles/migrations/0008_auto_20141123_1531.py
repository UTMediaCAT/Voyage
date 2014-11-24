# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20141111_0157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='source',
            old_name='source',
            new_name='url',
        ),
        migrations.AddField(
            model_name='article',
            name='url_origin',
            field=models.URLField(default='www.default.site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='url_origin',
            field=models.URLField(default='www.default.site'),
            preserve_default=False,
        ),
    ]
