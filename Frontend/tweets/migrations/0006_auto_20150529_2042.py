# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_auto_20141125_0056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keyword',
            old_name='keyword',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='tweet',
            old_name='user',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='source',
            old_name='url_origin',
	    new_name='domain',
        ),
    ]
