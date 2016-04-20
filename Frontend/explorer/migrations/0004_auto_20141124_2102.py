# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0003_auto_20141110_2325'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taccount',
            options={'verbose_name': 'Twitter Account'},
        ),
        migrations.RemoveField(
            model_name='fsite',
            name='influence',
        ),
        migrations.RemoveField(
            model_name='msite',
            name='influence',
        ),
        migrations.AlterField(
            model_name='fsite',
            name='name',
            field=models.CharField(help_text=b'Your favorable alias of this site.', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsite',
            name='url',
            field=models.URLField(help_text=b'Must include "http://", and try to the url as simple as possible for maximum matches.\nMaximum 2000 characters', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keyword',
            name='keyword',
            field=models.CharField(help_text=b'Case insensitive.\nMaximum 200 characters', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='msite',
            name='name',
            field=models.CharField(help_text=b'Your favorable alias of this site.\nMaximum 200 characters', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='msite',
            name='url',
            field=models.URLField(help_text=b'Must include "http://", and try to the url as simple as possible for maximum matches.\nMaximum 2000 characters', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taccount',
            name='account',
            field=models.CharField(help_text=b'Do not include "@", Ex. CNN\nMaximum 200 characters', unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
