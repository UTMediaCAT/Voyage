# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0017_auto_20160207_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Case insensitive. Maximum 200 characters (Ex. Canada)', unique=True, max_length=200)),
                ('keyword', models.ForeignKey(to='explorer.Keyword')),
            ],
            options={
                'verbose_name': 'Alias',
                'verbose_name_plural': 'Aliases',
            },
            bases=(models.Model,),
        ),
    ]
