# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import explorer.models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0022_auto_20160219_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceTwitterAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(help_text=b'Do not include "@". Maximum 15 characters (Ex. CNN)', unique=True, max_length=200, validators=[explorer.models.validate_user])),
                ('primary', models.ForeignKey(to='explorer.SourceTwitter')),
            ],
            options={
                'verbose_name': 'Alias',
                'verbose_name_plural': 'Aliases',
            },
            bases=(models.Model,),
        ),
    ]
