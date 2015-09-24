# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0011_auto_20150720_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferringSiteFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(help_text=b'Any URL that matches the pattern will be ignored from the crawler.', max_length=1000)),
                ('regex', models.BooleanField(default=False, help_text=b'Use Regular Expression')),
                ('site', models.ForeignKey(to='explorer.ReferringSite')),
            ],
            options={
                'verbose_name': 'Filter',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='referringsite',
            name='check',
            field=models.BooleanField(default=True, help_text=b'Check to display the amount of articles found by Newspaper (Displays as error).<br>Uncheck to save without testing Newspaper.', verbose_name=b'Check Newspaper'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referringsite',
            name='mode',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'Newspaper - Fast but may not work on some sites. Use Check Newspaper to determine the compatibility<br>Plan B - Slow but compatible with any sites.<br>Both - Uses both Newspaper and Plan B for maximum results.', verbose_name=b'Crawler', choices=[(0, b'Newspaper'), (1, b'Plan B'), (2, b'Both')]),
            preserve_default=True,
        ),
    ]
