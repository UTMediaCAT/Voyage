# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forwards(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Version = apps.get_model("articles", "Version")
    db_alias = schema_editor.connection.alias

    for article in Article.objects.using(db_alias).all():
        version = Version.objects.using(db_alias).create(
            article=article,
            title=article.title,
            text=article.text,
            text_hash=article.text_hash,
            language=article.language,
            date_added=article.date_added,
            date_last_seen=article.date_last_seen,
            date_published=article.date_published,
            found_by=article.found_by)

        for author in article.author_set.using(db_alias).all():
            author.version = version
            author.save()

        for sourceSite in article.sourcesite_set.using(db_alias).all():
            sourceSite.version = version
            sourceSite.save()

        for sourceTwitter in article.sourcetwitter_set.using(db_alias).all():
            sourceTwitter.version = version
            sourceTwitter.save()

        for keyword in article.keyword_set.using(db_alias).all():
            keyword.version = version
            keyword.save()

        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0023_auto_20160320_1845'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
