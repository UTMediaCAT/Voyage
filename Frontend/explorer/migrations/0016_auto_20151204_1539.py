# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0015_auto_20151118_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referringsite',
            name='check',
            field=models.BooleanField(default=False, help_text=b'Check to display the amount of articles found by Newspaper RSS Scan (Displays as error).<br>Uncheck to save without testing Newspaper.', verbose_name=b'Test Newspaper RSS Scan'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referringsite',
            name='mode',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'Newspaper - Fast but may not work on some sites. Use Check Newspaper to determine the compatibility<br>MediaCAT Crawler - Slow but compatible with any sites.<br>Both - Uses both Newspaper and MediaCAT CrawlerB for maximum results.', verbose_name=b'Scanner', choices=[(0, b'Newspaper'), (1, b'MediaCAT Crawler'), (2, b'Both')]),
            preserve_default=True,
        ),
    ]
