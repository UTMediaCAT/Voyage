# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0018_keywordalias'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceSiteAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.URLField(help_text=b'Must include "http://", and choose the url as simple as possible for maximum matches. Maximum 2000 characters (Ex. http://aljazeera.com)', unique=True, max_length=2000)),
                ('primary', models.ForeignKey(to='explorer.SourceSite')),
            ],
            options={
                'verbose_name': 'Source Site',
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='keywordalias',
            old_name='name',
            new_name='alias',
        ),
        migrations.RenameField(
            model_name='keywordalias',
            old_name='keyword',
            new_name='primary',
        ),
    ]
