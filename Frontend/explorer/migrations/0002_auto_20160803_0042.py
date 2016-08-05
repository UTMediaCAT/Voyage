# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Frontend.fields


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referringsite',
            name='url',
            field=Frontend.fields.URLProtocolField(help_text=b'Choose a simple URL to maximize matches. Maximum 2000 characters (Ex. http://cnn.com)', unique=True, max_length=2000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sourcesite',
            name='url',
            field=Frontend.fields.URLProtocolField(help_text=b'Choose a simple URL to maximize matches. Maximum 2000 characters (Ex. http://aljazeera.com)', unique=True, max_length=2000),
            preserve_default=True,
        ),
    ]
