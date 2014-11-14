# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20141110_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_added',
            field=models.DateField(null=True, verbose_name=b'Date Added'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='date_published',
            field=models.DateField(null=True, verbose_name=b'Date Published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='influence',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
