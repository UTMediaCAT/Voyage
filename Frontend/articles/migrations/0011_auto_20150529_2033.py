# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_auto_20141125_0055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='author',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='keyword',
            old_name='keyword',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='url_origin',
	    new_name='domain',
        ),
        migrations.RenameField(
            model_name='source',
            old_name='url_origin',
	    new_name='domain',
        ),
	migrations.RemoveField(
            model_name='article',
            name='influence',
        ),
    ]
