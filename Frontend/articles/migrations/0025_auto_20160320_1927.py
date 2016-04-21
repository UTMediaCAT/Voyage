# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0024_migrate_text_to_versions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='article',
            name='date_last_seen',
        ),
        migrations.RemoveField(
            model_name='article',
            name='date_modified',
        ),
        migrations.RemoveField(
            model_name='article',
            name='date_published',
        ),
        migrations.RemoveField(
            model_name='article',
            name='found_by',
        ),
        migrations.RemoveField(
            model_name='article',
            name='language',
        ),
        migrations.RemoveField(
            model_name='article',
            name='text',
        ),
        migrations.RemoveField(
            model_name='article',
            name='text_hash',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title',
        ),
        migrations.RemoveField(
            model_name='author',
            name='article',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='article',
        ),
        migrations.RemoveField(
            model_name='sourcesite',
            name='article',
        ),
        migrations.RemoveField(
            model_name='sourcetwitter',
            name='article',
        ),
    ]
