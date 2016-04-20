# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import explorer.models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0007_auto_20150529_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceTwitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Do not include "@". Maximum 15 characters (Ex. CNN)', unique=True, max_length=200, validators=[explorer.models.validate_user])),
            ],
            options={
                'verbose_name': 'Source Twitter Account',
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='TwitterAccount',
            new_name='ReferringTwitter',
        ),
        migrations.AlterModelOptions(
            name='referringtwitter',
            options={'verbose_name': 'Referring Twitter Account'},
        ),
    ]
