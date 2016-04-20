# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0025_auto_20160414_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referringsite',
            name='url',
            field=models.URLField(help_text=b'Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://cnn.com)', unique=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sourcesite',
            name='url',
            field=models.URLField(help_text=b'Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://aljazeera.com)', unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
