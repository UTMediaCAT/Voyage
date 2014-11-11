# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fsite',
            name='url',
            field=models.URLField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keyword',
            name='keyword',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='msite',
            name='url',
            field=models.URLField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taccount',
            name='account',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
