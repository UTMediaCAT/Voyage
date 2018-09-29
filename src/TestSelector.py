#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'Frontend')))
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'
# For Models connecting with the Django Database
from explorer.models import *
from ExplorerArticle import ExplorerArticle

if __name__ == "__main__":
    id = eval(input("site id: "))
    django.setup()
    site = ReferringSite.objects.get(pk=id)
    url = eval(input("url: "))
    article = ExplorerArticle(url)
    article.download()
    article.preliminary_parse()
    article.newspaper_parse()

    fields = {}
    for css in site.referringsitecssselector_set.all():
        if not (css.field_choice in list(fields.keys())):
            fields[css.field_choice] = []

        fields[css.field_choice].append({'pattern': css.pattern, 'regex': css.regex})
    if(not len(list(fields.keys()))):
        print("no fields")

    for key, value in fields.items():
        print("field \"{0}\"".format(key))
        print(article.evaluate_css_selectors(value))
        print()