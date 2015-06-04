"""
This script retrieves and organizes data collected by explorer into
arrays and dictionaries to make it an appropriate input for
graphs and trees in the JIT library
"""

__author__ = "ACME: CSCC01F14 Team 4"

import django
import re

from articles.models import*
from articles.models import Keyword as ArticleKeyword
from articles.models import Source as ArticleSource
from explorer.models import*
from explorer.models import Keyword as ExplorerKeyword
from tweets.models import*
from tweets.models import Keyword as TwitterKeyword
from tweets.models import Source as TwitterSource


def article_hypertree():
    '''(None) -> dict of dict of dict of obj
    Filters articles per referring site and generates a
    3d dict of relation with the source site that is used by
    JIT graphing library to create graph
    '''
    msites = []

    # for all the referring sites
    for msite in ReferringSite.objects.all():
        # create a node with an empty array for the children
        data = {}
        data["id"] = msite.url
        data["name"] = msite.name
        data["children"] = []
        data["data"] = {"relation": "Sourced"}

        fsites_dict = {}
        # gets all articles that match msite
        for article in Article.objects.filter(domain=msite.url):
            fsites = ArticleSource.objects.filter(article=article)

            for fsite in fsites:
                fsite_name = (SourceSite.objects.get(url=fsite.domain)).name
                if fsite_name in fsites_dict.keys():
                    fsites_dict[fsite_name].append(fsite)
                else:
                    fsites_dict[fsite_name] = [fsite]

        # create the fsite dict that is readable by JIT graph library
        for fsite in fsites_dict.keys():
            fsites_data = {}
            fsites_data["id"] = fsite
            fsites_data["name"] = fsite
            fsites_data["children"] = []
            fsites_data["data"] = {"relation": "Sourced"}
            data["children"].append(fsites_data)

        msites.append(data)

    data = {"id": "ReferringSites", "name": "Referring Sites", "children": msites,
            "relation": "Referring Sites"}

    return data


def article_spacetree(site):
    '''(str) -> dict of dict of dict of obj
    Filters articles per referring site and generates a
    3d dict of relation with the keywords that is used by
    JIT graphing library to create graph
    '''
    data = []
    if site is None:
        msites = ReferringSite.objects.all()
    else:
        msites = ReferringSite.objects.filter(name=site)

    # for all the referring sites matching the site
    for msite in msites:
        # create a node with an empty array for the children
        site_data = {}
        site_data["id"] = msite.url
        site_data["name"] = msite.name
        site_data["children"] = []
        site_data["data"] = {"relation": "Sourced"}

        keywords_dict = {}
        # gets all articles that match msite
        for article in Article.objects.filter(domain=msite.url):
            keywords = ArticleKeyword.objects.filter(article=article)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

        # create the fsite dict that is readable by JIT graph library
        for keyword in keywords_dict.keys():
            # create a node with an empty array for the children
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["children"] = []
            keywords_data["data"] = {"relation": "Sourced"}
            site_data["children"].append(keywords_data)

        data.append(site_data)

    if site is None:
        data = {
            "id": "ReferringSites",
            "name": "Referring Sites",
            "children": data,
            "relation": "Referring Sites"}
    else:
        if len(data) != 0:
            data = data[0]
        else:
            data = []

    return data, ReferringSite.objects.all()


def article_weightedtree(site):
    '''(str) -> dict of dict of dict of obj
    Filters articles per referring site and generates a
    3d dict of relation with the keywords and source sites that is used by
    JIT graphing library to create graph
    '''
    msites = []
    max_dim = 1

    if site is None:
        results = ReferringSite.objects.all()
    else:
        results = ReferringSite.objects.filter(name=site)

    for msite in results:
        # create a node with an empty array for the children
        data = {}
        data["id"] = msite.url
        data["name"] = msite.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        fsites_dict = {}
        for article in Article.objects.filter(domain=msite.url):
            keywords = ArticleKeyword.objects.filter(article=article)
            fsites = ArticleSource.objects.filter(article=article)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

            for fsite in fsites:
                if fsite.domain in fsites_dict.keys():
                    fsites_dict[fsite.domain].append(fsite)
                else:
                    fsites_dict[fsite.domain] = [fsite]

        for keyword in keywords_dict.keys():
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["nodeTo"] = keyword

            data["adjacencies"].append(keywords_data)
            data["data"]["$dim"] += len(keywords_dict[keyword])
            keywords_data_info = keywords_data.copy()
            keywords_data_info["data"] = {
                "$dim": len(
                    keywords_dict[keyword]),
                "$type": "square",
                "$color": "#00AA00"}
            msites.append(keywords_data_info)

        for fsite in fsites_dict.keys():
            fsites_data = {}
            fsites_data["id"] = fsite
            fsites_data["name"] = fsite
            fsites_data["nodeTo"] = fsite

            data["adjacencies"].append(fsites_data)
            data["data"]["$dim"] += len(fsites_dict[fsite])
            fsites_data_info = fsites_data.copy()
            fsites_data_info["data"] = {
                "$dim": len(
                    fsites_dict[fsite]),
                "$type": "circle",
                "$color": "#FF0000"}
            msites.append(fsites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        if len(data["adjacencies"]) > 0:
            msites.append(data)

    for msite in msites:
        msite["data"]["$dim"] = int(
            msite["data"]["$dim"] * 30.0 / max_dim) + 10

    return msites, ReferringSite.objects.all()


def article_forcegraph(site):
    '''(str) -> dict of dict of dict of obj
    Filters articles per referring site and generates a
    3d dict of relation with the keywords and source sites that is used by
    JIT graphing library to create graph
    '''
    msites = []
    max_dim = 1

    if site is None:
        results = ReferringSite.objects.all()
    else:
        results = ReferringSite.objects.filter(name=site)

    for msite in results:
        # create a node with an empty array for the children
        data = {}
        data["id"] = msite.url
        data["name"] = msite.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        fsites_dict = {}
        for article in Article.objects.filter(domain=msite.url):
            keywords = ArticleKeyword.objects.filter(article=article)
            fsites = ArticleSource.objects.filter(article=article)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

            for fsite in fsites:
                if fsite.domain in fsites_dict.keys():
                    fsites_dict[fsite.domain].append(fsite)
                else:
                    fsites_dict[fsite.domain] = [fsite]

        for keyword in keywords_dict.keys():
            # create a node with an empty array for the children
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["nodeTo"] = keyword

            data["adjacencies"].append(keywords_data)
            data["data"]["$dim"] += len(keywords_dict[keyword])
            keywords_data_info = keywords_data.copy()
            keywords_data_info["data"] = {
                "$dim": len(
                    keywords_dict[keyword]),
                "$type": "square",
                "$color": "#00AA00"}
            msites.append(keywords_data_info)

        for fsite in fsites_dict.keys():
            # create a node with an empty array for the children
            fsites_data = {}
            fsites_data["id"] = fsite
            fsites_data["name"] = fsite
            fsites_data["nodeTo"] = fsite

            data["adjacencies"].append(fsites_data)
            data["data"]["$dim"] += len(fsites_dict[fsite])
            fsites_data_info = fsites_data.copy()
            fsites_data_info["data"] = {
                "$dim": len(
                    fsites_dict[fsite]),
                "$type": "circle",
                "$color": "#FF0000"}
            msites.append(fsites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        if len(data["adjacencies"]) > 0:
            msites.append(data)

    for msite in msites:
        msite["data"]["$dim"] = int(
            msite["data"]["$dim"] * 30.0 / max_dim) + 10

    return msites, ReferringSite.objects.all()


def tweet_hypertree():
    '''(str) -> dict of dict of dict of obj
    Filters tweets per referring twitter account and generates a
    3d dict of relation with the source sites that is used by
    JIT graphing library to create graph
    '''
    taccounts = []

    for account in TwitterAccount.objects.all():
        # create a node with an empty array for the children
        data = {}
        data["id"] = account.name
        data["name"] = account.name
        data["children"] = []
        data["data"] = {"relation": "Sourced"}

        fsites_dict = {}
        for tweet in Tweet.objects.filter(name=account.name):
            fsites = TwitterSource.objects.filter(tweet=tweet)

            for fsite in fsites:
                fsite_name = (SourceSite.objects.get(url=fsite.domain)).name
                if fsite_name in fsites_dict.keys():
                    fsites_dict[fsite_name].append(fsite)
                else:
                    fsites_dict[fsite_name] = [fsite]

        for fsite in fsites_dict.keys():
            # create a node with an empty array for the children
            fsites_data = {}
            fsites_data["id"] = fsite
            fsites_data["name"] = fsite
            fsites_data["children"] = []
            fsites_data["data"] = {"relation": "Sourced"}
            data["children"].append(fsites_data)

        taccounts.append(data)

    data = {
        "id": "TwitterAccounts",
        "name": "Twitter Accounts",
        "children": taccounts,
        "relation": "Referring Twitter Accounts"}

    return data


def tweet_spacetree(account):
    '''(str) -> dict of dict of dict of obj
    Filters tweets per referring twitter account and generates a
    3d dict of relation with the keywords that is used by
    JIT graphing library to create graph
    '''
    data = []
    if account is None:
        taccounts = TwitterAccount.objects.all()
    else:
        taccounts = TwitterAccount.objects.filter(name=account)

    for taccount in taccounts:
        account_data = {}
        account_data["id"] = taccount.name
        account_data["name"] = taccount.name
        account_data["children"] = []
        account_data["data"] = {"relation": "Sourced"}

        keywords_dict = {}
        for tweet in Tweet.objects.filter(name=taccount.name):
            keywords = TwitterKeyword.objects.filter(tweet=tweet)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

        for keyword in keywords_dict.keys():
            # create a node with an empty array for the children
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["children"] = []
            keywords_data["data"] = {"relation": "Sourced"}
            account_data["children"].append(keywords_data)

        data.append(account_data)

    if account is None:
        data = {"id": "TwitterAccounts", "name": "Twitter Accounts",
                "children": data, "relation": "Referring Twitter Accounts"}
    else:
        if len(data) != 0:
            data = data[0]
        else:
            data = []

    return data, TwitterAccount.objects.all()


def tweet_weightedtree(account):
    '''(str) -> dict of dict of dict of obj
    Filters tweets per referring twitter account and generates a
    3d dict of relation with the keywords and source sites that is used by
    JIT graphing library to create graph
    '''
    taccounts = []
    max_dim = 1

    if account is None:
        results = TwitterAccount.objects.all()
    else:
        results = TwitterAccount.objects.filter(name=account)

    for taccount in results:
        # create a node with an empty array for the children
        data = {}
        data["id"] = taccount.name
        data["name"] = taccount.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        fsites_dict = {}
        for tweet in Tweet.objects.filter(name=taccount.name):
            keywords = TwitterKeyword.objects.filter(tweet=tweet)
            fsites = TwitterSource.objects.filter(tweet=tweet)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

            for fsite in fsites:
                if fsite.domain in fsites_dict.keys():
                    fsites_dict[fsite.domain].append(fsite)
                else:
                    fsites_dict[fsite.domain] = [fsite]

        for keyword in keywords_dict.keys():
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["nodeTo"] = keyword

            data["adjacencies"].append(keywords_data)
            data["data"]["$dim"] += len(keywords_dict[keyword])
            keywords_data_info = keywords_data.copy()
            keywords_data_info["data"] = {
                "$dim": len(
                    keywords_dict[keyword]),
                "$type": "square",
                "$color": "#00AA00"}
            taccounts.append(keywords_data_info)

        for fsite in fsites_dict.keys():
            fsites_data = {}
            fsites_data["id"] = fsite
            fsites_data["name"] = fsite
            fsites_data["nodeTo"] = fsite

            data["adjacencies"].append(fsites_data)
            data["data"]["$dim"] += len(fsites_dict[fsite])
            fsites_data_info = fsites_data.copy()
            fsites_data_info["data"] = {
                "$dim": len(
                    fsites_dict[fsite]),
                "$type": "circle",
                "$color": "#FF0000"}
            taccounts.append(fsites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        if len(data["adjacencies"]) > 0:
            taccounts.append(data)

    for taccount in taccounts:
        taccount["data"]["$dim"] = int(
            taccount["data"]["$dim"] * 30.0 / max_dim) + 10

    return taccounts, TwitterAccount.objects.all()


def tweet_forcegraph(account):
    '''(str) -> dict of dict of dict of obj
    Filters tweets per referring twitter account and generates a
    3d dict of relation with the keywords and source sites that is used by
    JIT graphing library to create graph
    '''
    taccounts = []
    max_dim = 1

    if account is None:
        results = TwitterAccount.objects.all()
    else:
        results = TwitterAccount.objects.filter(name=account)

    for taccount in results:
        # create a node with an empty array for the adjacencies
        data = {}
        data["id"] = taccount.name
        data["name"] = taccount.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        fsites_dict = {}
        for tweet in Tweet.objects.filter(name=taccount.name):
            keywords = TwitterKeyword.objects.filter(tweet=tweet)
            fsites = TwitterSource.objects.filter(tweet=tweet)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

            for fsite in fsites:
                if fsite.domain in fsites_dict.keys():
                    fsites_dict[fsite.domain].append(fsite)
                else:
                    fsites_dict[fsite.domain] = [fsite]

        for keyword in keywords_dict.keys():
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["nodeTo"] = keyword

            data["adjacencies"].append(keywords_data)
            data["data"]["$dim"] += len(keywords_dict[keyword])
            keywords_data_info = keywords_data.copy()
            keywords_data_info["data"] = {
                "$dim": len(
                    keywords_dict[keyword]),
                "$type": "square",
                "$color": "#00AA00"}
            taccounts.append(keywords_data_info)

        for fsite in fsites_dict.keys():
            fsites_data = {}
            fsites_data["id"] = fsite
            fsites_data["name"] = fsite
            fsites_data["nodeTo"] = fsite

            data["adjacencies"].append(fsites_data)
            data["data"]["$dim"] += len(fsites_dict[fsite])
            fsites_data_info = fsites_data.copy()
            fsites_data_info["data"] = {
                "$dim": len(
                    fsites_dict[fsite]),
                "$type": "circle",
                "$color": "#FF0000"}
            taccounts.append(fsites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        if len(data["adjacencies"]) > 0:
            taccounts.append(data)

    for taccount in taccounts:
        taccount["data"]["$dim"] = int(
            taccount["data"]["$dim"] * 30.0 / max_dim) + 10

    return taccounts, TwitterAccount.objects.all()
