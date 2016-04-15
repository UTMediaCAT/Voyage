# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0023_sourcetwitteralias'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sourcesitealias',
            name='name',
        ),
        migrations.AlterField(
            model_name='sourcesitealias',
            name='alias',
            field=models.CharField(help_text=b'Case insensitive. Maximum 200 characters (Ex. Canada)', unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
