# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0006_auto_20141126_0048'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Msite',
            new_name='ReferringSite',
        ),
        migrations.RenameModel(
            old_name='Fsite',
            new_name='SourceSite',
        ),
        migrations.RenameModel(
            old_name='Taccount',
            new_name='TwitterAccount',
        ),
        migrations.AlterModelOptions(
            name='referringsite',
            options={'verbose_name': 'Referring Site'},
        ),
        migrations.AlterModelOptions(
            name='sourcesite',
            options={'verbose_name': 'Source Site'},
        ),
        migrations.RenameField(
            model_name='keyword',
            old_name='keyword',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='twitteraccount',
            old_name='account',
            new_name='name',
        ),
    ]
