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
from articles.models import SourceSite as ArticleSourceSite
from explorer.models import*
from explorer.models import Keyword as ExplorerKeyword
from explorer.models import SourceTwitter as ExplorerSourceTwitter
from tweets.models import*
from tweets.models import Keyword as TwitterKeyword
from tweets.models import SourceSite as TwitterSourceSite


def article_hypertree():
    '''(None) -> dict of dict of dict of obj
    Filters articles per referring site and generates a
    3d dict of relation with the source site that is used by
    JIT graphing library to create graph
    '''
    rsites = []

    # for all the referring sites
    for rsite in ReferringSite.objects.all():
        # create a node with an empty array for the children
        data = {}
        data["id"] = rsite.url
        data["name"] = rsite.name
        data["children"] = []
        data["data"] = {"relation": "Sourced"}

        ssites_dict = {}
        # gets all articles that match rsite
        for article in Article.objects.filter(domain=rsite.url):
            ssites = ArticleSourceSite.objects.filter(article=article)

            for ssite in ssites:
                ssite_name = (ArticleSourceSite.objects.get(url=ssite.domain)).name
                if ssite_name in ssites_dict.keys():
                    ssites_dict[ssite_name].append(ssite)
                else:
                    ssites_dict[ssite_name] = [ssite]

        # create the ssite dict that is readable by JIT graph library
        for ssite in ssites_dict.keys():
            ssites_data = {}
            ssites_data["id"] = ssite
            ssites_data["name"] = ssite
            ssites_data["children"] = []
            ssites_data["data"] = {"relation": "Sourced"}
            data["children"].append(ssites_data)

        rsites.append(data)

    data = {"id": "ReferringSites", "name": "Referring Sites", "children": rsites,
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
        rsites = ReferringSite.objects.all()
    else:
        rsites = ReferringSite.objects.filter(name=site)

    # for all the referring sites matching the site
    for rsite in rsites:
        # create a node with an empty array for the children
        site_data = {}
        site_data["id"] = rsite.url
        site_data["name"] = rsite.name
        site_data["children"] = []
        site_data["data"] = {"relation": "Sourced"}

        keywords_dict = {}
        # gets all articles that match rsite
        for article in Article.objects.filter(domain=rsite.url):
            keywords = ArticleKeyword.objects.filter(article=article)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

        # create the ssite dict that is readable by JIT graph library
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
    rsites = []
    max_dim = 1

    if site is None:
        results = ReferringSite.objects.all()
    else:
        results = ReferringSite.objects.filter(name=site)

    for rsite in results:
        # create a node with an empty array for the children
        data = {}
        data["id"] = rsite.url
        data["name"] = rsite.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        ssites_dict = {}
        for article in Article.objects.filter(domain=rsite.url):
            keywords = ArticleKeyword.objects.filter(article=article)
            ssites = ArticleSourceSite.objects.filter(article=article)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

            for ssite in ssites:
                if ssite.domain in ssites_dict.keys():
                    ssites_dict[ssite.domain].append(ssite)
                else:
                    ssites_dict[ssite.domain] = [ssite]

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
            rsites.append(keywords_data_info)

        for ssite in ssites_dict.keys():
            ssites_data = {}
            ssites_data["id"] = ssite
            ssites_data["name"] = ssite
            ssites_data["nodeTo"] = ssite

            data["adjacencies"].append(ssites_data)
            data["data"]["$dim"] += len(ssites_dict[ssite])
            ssites_data_info = ssites_data.copy()
            ssites_data_info["data"] = {
                "$dim": len(
                    ssites_dict[ssite]),
                "$type": "circle",
                "$color": "#FF0000"}
            rsites.append(ssites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        if len(data["adjacencies"]) > 0:
            rsites.append(data)

    for rsite in rsites:
        rsite["data"]["$dim"] = int(
            rsite["data"]["$dim"] * 30.0 / max_dim) + 10

    return rsites, ReferringSite.objects.all()


def article_forcegraph(site):
    '''(str) -> dict of dict of dict of obj
    Filters articles per referring site and generates a
    3d dict of relation with the keywords and source sites that is used by
    JIT graphing library to create graph
    '''
    rsites = []
    max_dim = 1

    if site is None:
        results = ReferringSite.objects.all()
    else:
        results = ReferringSite.objects.filter(name=site)

    for rsite in results:
        # create a node with an empty array for the children
        data = {}
        data["id"] = rsite.url
        data["name"] = rsite.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        ssites_dict = {}
        for article in Article.objects.filter(domain=rsite.url):
            keywords = ArticleKeyword.objects.filter(article=article)
            ssites = ArticleSourceSite.objects.filter(article=article)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

            for ssite in ssites:
                if ssite.domain in ssites_dict.keys():
                    ssites_dict[ssite.domain].append(ssite)
                else:
                    ssites_dict[ssite.domain] = [ssite]

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
            rsites.append(keywords_data_info)

        for ssite in ssites_dict.keys():
            # create a node with an empty array for the children
            ssites_data = {}
            ssites_data["id"] = ssite
            ssites_data["name"] = ssite
            ssites_data["nodeTo"] = ssite

            data["adjacencies"].append(ssites_data)
            data["data"]["$dim"] += len(ssites_dict[ssite])
            ssites_data_info = ssites_data.copy()
            ssites_data_info["data"] = {
                "$dim": len(
                    ssites_dict[ssite]),
                "$type": "circle",
                "$color": "#FF0000"}
            rsites.append(ssites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        if len(data["adjacencies"]) > 0:
            rsites.append(data)

    for rsite in rsites:
        rsite["data"]["$dim"] = int(
            rsite["data"]["$dim"] * 30.0 / max_dim) + 10

    return rsites, ReferringSite.objects.all()


def tweet_hypertree():
    '''(str) -> dict of dict of dict of obj
    Filters tweets per referring twitter account and generates a
    3d dict of relation with the source sites that is used by
    JIT graphing library to create graph
    '''
    taccounts = []

    for account in ExplorerSourceTwitter.objects.all():
        # create a node with an empty array for the children
        data = {}
        data["id"] = account.name
        data["name"] = account.name
        data["children"] = []
        data["data"] = {"relation": "Sourced"}

        ssites_dict = {}
        for tweet in Tweet.objects.filter(name=account.name):
            ssites = TwitterSourceSite.objects.filter(tweet=tweet)

            for ssite in ssites:
                ssite_name = (TwitterSourceSite.objects.get(url=ssite.domain)).name
                if ssite_name in ssites_dict.keys():
                    ssites_dict[ssite_name].append(ssite)
                else:
                    ssites_dict[ssite_name] = [ssite]

        for ssite in ssites_dict.keys():
            # create a node with an empty array for the children
            ssites_data = {}
            ssites_data["id"] = ssite
            ssites_data["name"] = ssite
            ssites_data["children"] = []
            ssites_data["data"] = {"relation": "Sourced"}
            data["children"].append(ssites_data)

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
        taccounts = ExplorerSourceTwitter.objects.all()
    else:
        taccounts = ExplorerSourceTwitter.objects.filter(name=account)

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

    return data, ExplorerSourceTwitter.objects.all()


def tweet_weightedtree(account):
    '''(str) -> dict of dict of dict of obj
    Filters tweets per referring twitter account and generates a
    3d dict of relation with the keywords and source sites that is used by
    JIT graphing library to create graph
    '''
    taccounts = []
    max_dim = 1

    if account is None:
        results = ExplorerSourceTwitter.objects.all()
    else:
        results = ExplorerSourceTwitter.objects.filter(name=account)

    for taccount in results:
        # create a node with an empty array for the children
        data = {}
        data["id"] = taccount.name
        data["name"] = taccount.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        ssites_dict = {}
        for tweet in Tweet.objects.filter(name=taccount.name):
            keywords = TwitterKeyword.objects.filter(tweet=tweet)
            ssites = TwitterSourceSite.objects.filter(tweet=tweet)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

            for ssite in ssites:
                if ssite.domain in ssites_dict.keys():
                    ssites_dict[ssite.domain].append(ssite)
                else:
                    ssites_dict[ssite.domain] = [ssite]

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

        for ssite in ssites_dict.keys():
            ssites_data = {}
            ssites_data["id"] = ssite
            ssites_data["name"] = ssite
            ssites_data["nodeTo"] = ssite

            data["adjacencies"].append(ssites_data)
            data["data"]["$dim"] += len(ssites_dict[ssite])
            ssites_data_info = ssites_data.copy()
            ssites_data_info["data"] = {
                "$dim": len(
                    ssites_dict[ssite]),
                "$type": "circle",
                "$color": "#FF0000"}
            taccounts.append(ssites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        if len(data["adjacencies"]) > 0:
            taccounts.append(data)

    for taccount in taccounts:
        taccount["data"]["$dim"] = int(
            taccount["data"]["$dim"] * 30.0 / max_dim) + 10

    return taccounts, ExplorerSourceTwitter.objects.all()


def tweet_forcegraph(account):
    '''(str) -> dict of dict of dict of obj
    Filters tweets per referring twitter account and generates a
    3d dict of relation with the keywords and source sites that is used by
    JIT graphing library to create graph
    '''
    taccounts = []
    max_dim = 1

    if account is None:
        results = ExplorerSourceTwitter.objects.all()
    else:
        results = ExplorerSourceTwitter.objects.filter(name=account)

    for taccount in results:
        # create a node with an empty array for the adjacencies
        data = {}
        data["id"] = taccount.name
        data["name"] = taccount.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        ssites_dict = {}
        for tweet in Tweet.objects.filter(name=taccount.name):
            keywords = TwitterKeyword.objects.filter(tweet=tweet)
            ssites = TwitterSourceSite.objects.filter(tweet=tweet)

            for keyword in keywords:
                if keyword.name in keywords_dict.keys():
                    keywords_dict[keyword.name].append(keyword)
                else:
                    keywords_dict[keyword.name] = [keyword]

            for ssite in ssites:
                if ssite.domain in ssites_dict.keys():
                    ssites_dict[ssite.domain].append(ssite)
                else:
                    ssites_dict[ssite.domain] = [ssite]

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

        for ssite in ssites_dict.keys():
            ssites_data = {}
            ssites_data["id"] = ssite
            ssites_data["name"] = ssite
            ssites_data["nodeTo"] = ssite

            data["adjacencies"].append(ssites_data)
            data["data"]["$dim"] += len(ssites_dict[ssite])
            ssites_data_info = ssites_data.copy()
            ssites_data_info["data"] = {
                "$dim": len(
                    ssites_dict[ssite]),
                "$type": "circle",
                "$color": "#FF0000"}
            taccounts.append(ssites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        if len(data["adjacencies"]) > 0:
            taccounts.append(data)

    for taccount in taccounts:
        taccount["data"]["$dim"] = int(
            taccount["data"]["$dim"] * 30.0 / max_dim) + 10

    return taccounts, ExplorerSourceTwitter.objects.all()
