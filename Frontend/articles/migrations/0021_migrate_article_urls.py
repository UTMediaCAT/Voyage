# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import hashlib

def hash_sha256(text):
    hash_text = hashlib.sha256()
    hash_text.update(text.encode('utf-8'))
    return hash_text.hexdigest()

def forwards(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Url = apps.get_model("articles", "Url")
    db_alias = schema_editor.connection.alias
    for article in Article.objects.using(db_alias).all():
        url = article.url
        Url.objects.using(db_alias).create(name=url, article=article)
        article.text_hash = hash_sha256(article.text)
        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_auto_20160306_2030'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
