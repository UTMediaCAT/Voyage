# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20150604_0316'),
    ]

    operations = [
	migrations.RenameModel('Source', 'SourceSite'),
	migrations.AddField('SourceSite', 'matched', models.BooleanField(default=True), preserve_default=False),
	migrations.AddField('SourceSite', 'local', models.BooleanField(default=False), preserve_default=False),
        migrations.CreateModel(
            name='SourceTwitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('matched', models.BooleanField()),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
