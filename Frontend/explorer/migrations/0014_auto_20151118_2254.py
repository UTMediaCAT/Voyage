# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0013_auto_20151112_0304'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferringSiteCssSelector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.PositiveSmallIntegerField(default=0, verbose_name=b'Field', choices=[(0, b'Title'), (1, b'Author'), (2, b'Date Published'), (3, b'Date Modified')])),
                ('pattern', models.CharField(help_text=b'CSS Selector pattern', max_length=1000)),
                ('regex', models.CharField(help_text=b'Regular expression to further narrow down', max_length=1000)),
                ('site', models.ForeignKey(to='explorer.ReferringSite')),
            ],
            options={
                'verbose_name': 'CSS Selectors',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='referringsitefilter',
            options={'verbose_name': 'Filters'},
        ),
        migrations.AlterField(
            model_name='referringsitefilter',
            name='regex',
            field=models.BooleanField(default=False, help_text=b'Use Regular Expression instead of string comparison.'),
            preserve_default=True,
        ),
    ]
