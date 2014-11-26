# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import explorer.models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0005_auto_20141125_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msite',
            name='url',
            field=models.URLField(help_text=b'Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://cnn.com)', unique=True, max_length=2000, validators=[explorer.models.validate_site]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taccount',
            name='account',
            field=models.CharField(help_text=b'Do not include "@". Maximum 15 characters (Ex. CNN)', unique=True, max_length=200, validators=[explorer.models.validate_user]),
            preserve_default=True,
        ),
    ]
