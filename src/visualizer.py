import django
import re

from articles.models import*
from articles.models import Keyword as A_Keyword
from articles.models import Source as A_Source
from explorer.models import*
from explorer.models import Keyword as E_Keyword
from tweets.models import*
from tweets.models import Keyword as T_Keyword

def article_hypertree():
    msites = []

    for msite in Msite.objects.all():
        data = {}
        data["id"] = msite.url
        data["name"] = msite.name
        data["children"] = []
        data["data"] = {"relation": "Sourced"}

        fsites_dict = {}
        for article in Article.objects.filter(url_origin = msite.url):
            fsites = A_Source.objects.filter(article = article)

            for fsite in fsites:
                if fsite.url_origin in fsites_dict.keys():
                    fsites_dict[fsite.url_origin].append(fsite)
                else:
                    fsites_dict[fsite.url_origin] = [fsite]   

        for fsite in fsites_dict.keys():
            fsites_data = {}
            fsites_data["id"] = fsite
            fsites_data["name"] = fsite
            fsites_data["children"] = []
            fsites_data["data"] = {"relation": "Sourced"}
            data["children"].append(fsites_data)

        msites.append(data)

    data = {"id": "Msites", "name": "Monitoring Sites", "children": msites, "relation": "Monitoring Sites"}

    return data

def article_spacetree():
    msites = []

    for msite in Msite.objects.all():
        data = {}
        data["id"] = msite.url
        data["name"] = msite.name
        data["children"] = []
        data["data"] = {"relation": "Sourced"}

        keywords_dict = {}
        fsites_dict = {}
        for article in Article.objects.filter(url_origin = msite.url):
            keywords = A_Keyword.objects.filter(article = article)

            for keyword in keywords:
                if keyword.keyword in keywords_dict.keys():
                    keywords_dict[keyword.keyword].append(keyword)
                else:
                    keywords_dict[keyword.keyword] = [keyword]
                
        for keyword in keywords_dict.keys():
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["children"] = []
            keywords_data["data"] = {"relation": "Sourced"}
            data["children"].append(keywords_data)

        msites.append(data)

    data = {"id": "Msites", "name": "Monitoring Sites", "children": msites, "relation": "Monitoring Sites"}

    return data

def article_weightedtree():
    msites = []

    for msite in Msite.objects.all():
        data = {}
        data["id"] = msite.url
        data["name"] = msite.name
        data["adjacencies"] = []
        data["data"] = {"$dim": msite.influence, "$type": "triangle"}

        keywords_dict = {}
        fsites_dict = {}
        for article in Article.objects.filter(url_origin = msite.url):
            keywords = A_Keyword.objects.filter(article = article)

            for keyword in keywords:
                if keyword.keyword in keywords_dict.keys():
                    keywords_dict[keyword.keyword].append(keyword)
                else:
                    keywords_dict[keyword.keyword] = [keyword]
                
        for keyword in keywords_dict.keys():
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["nodeTo"] = msite.url
            keywords_data["data"] = {"name": keyword, "weight": len(keywords_dict[keyword])}
            data["adjacencies"].append(keywords_data)

        msites.append(data)

    data = msites
    print data
    data = [{
                "id": "node0",
                "name": "node0 name",
                "data": {
                    "$dim": 16.759175934208628,
                    "some other key": "some other value"
                },
                "adjacencies": [{
                    "nodeTo": "node1",
                    "data": {
                        "weight": 3
                    }
                }, {
                    "nodeTo": "node2",
                    "data": {
                        "weight": 3
                    }
                }, {
                    "nodeTo": "node3",
                    "data": {
                        "weight": 3
                    }
                }]
            }, {
                "id": "node1",
                "name": "node1 name",
                "data": {
                    "$dim": 13.077119090372014,
                    "$type": "square",
                    "some other key": "some other value"
                },
                "adjacencies": [{
                    "nodeTo": "node0",
                    "data": {
                        "weight": 3
                    }
                }, {
                    "nodeTo": "node2",
                    "data": {
                        "weight": 1
                    }
                }, {
                    "nodeTo": "node3",
                    "data": {
                        "weight": 3
                    }
                }]
            }, {
                "id": "node2",
                "name": "node2 name",
                "data": {
                    "$dim": 24.937383149648717,
                    "$type": "triangle",
                    "some other key": "some other value"
                },
                "adjacencies": [{
                    "nodeTo": "node0",
                    "data": {
                        "weight": 3
                    }
                }, {
                    "nodeTo": "node1",
                    "data": {
                        "weight": 1
                    }
                }, {
                    "nodeTo": "node3",
                    "data": {
                        "weight": 3
                    }
                }]
            }, {
                "id": "node3",
                "name": "node3 name",
                "data": {
                    "$dim": 10.53272740718869,
                    "some other key": "some other value"
                },
                "adjacencies": [{
                    "nodeTo": "node0",
                    "data": {
                        "weight": 3
                    }
                }, {
                    "nodeTo": "node1",
                    "data": {
                        "weight": 3
                    }
                }, {
                    "nodeTo": "node2",
                    "data": {
                        "weight": 3
                    }
                }]
            }]
    return data

def article_rgraph():
    msites = []

    for msite in Msite.objects.all():
        data = {}
        data["id"] = msite.url
        data["name"] = msite.name
        data["children"] = []
        data["data"] = {"relation": "Sourced"}

        keywords_dict = {}
        fsites_dict = {}
        for article in Article.objects.filter(url_origin = msite.url):
            keywords = A_Keyword.objects.filter(article = article)

            for keyword in keywords:
                if keyword.keyword in keywords_dict.keys():
                    keywords_dict[keyword.keyword].append(keyword)
                else:
                    keywords_dict[keyword.keyword] = [keyword]
                
        for keyword in keywords_dict.keys():
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["children"] = []
            keywords_data["data"] = {"relation": "Sourced"}
            data["children"].append(keywords_data)

        msites.append(data)

    data = {"id": "Msites", "name": "Monitoring Sites", "children": msites, "relation": "Monitoring Sites"}

    return data

def article_forcegraph():
    data = {}

    return data

def tweet_hypertree():
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

def tweet_spacetree():
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

def tweet_weightedtree():
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

def tweet_rgraph():
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

def tweet_forcegraph():
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

def keywords_pie_chart():
    data_dict = {}
     
    if is_A:
        keywords = A_Keyword.objects.all()
    else:
        keywords = T_Keyword.objects.all()
    for ele in keywords:
        if not ele.keyword in data_dict.keys():
            data_dict[ele.keyword] = 1
        else:
            data_dict[ele.keyword] += 1

    data = []
    for ele in data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(data_dict[ele])
        data.append(new)

    return data

def articles_annotation_chart():
    article_by_date = []
    sites = []
    for s in Msite.objects.all():
        sites.append(re.search("([a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.)+[a-zA-Z]{2,6}",
                     s.url, re.IGNORECASE).group(0).encode("ascii"))

    for art in Article.objects.all():
        added = False
        date = art.date_added.strftime("%B %d, %Y")
        for index in range(len(article_by_date)):
            if date == article_by_date[index][0]:
                added = True
                for i in range(len(sites)):
                    if sites[i] in art.url.encode("ascii"):
                        article_by_date[index][i+1] += 1
                        break
            if added:
                break

        if not added:
            article_by_date.append([date] + [0]*len(sites))
            for i in range(len(sites)):
                if sites[i] in art.url:
                    article_by_date[-1][i+1] += 1
                    break

    return sites, article_by_date


def msites_bar_chart():

    data = []
    data.append (["Foreign Sites", "Number of source matched"])


    fsites = Fsite.objects.all()
    for site in fsites:
        source_number = A_Source.objects.filter(url_origin = site.url).count()
        data.append([site.name.encode("utf-8"), source_number])
    return data




def tweets_annotation_chart():
    Taccounts  = Taccount.objects.all()
    accounts = []
    for element in Taccounts:
        accounts.append(element.account.encode("utf-8"))

    data = []

    pre_date = None

    for twt in Tweet.objects.all():
        new=[]
        date = twt.date_added.strftime("%B %d, %Y")
        if date == pre_date:
            break;
        else:
            pre_date = date
            new.append(date)
            for account in accounts:
                new.append(Tweet.objects.filter(date_added = twt.date_added).count())
            data.append(new)
    return accounts, data


def follower_bar_chart():

    data = []
    data.append (["Foreign Sites","Number of source matched"])

    accounts = Taccount.objects.all()
    for account in accounts:
        twts = Tweet.objects.filter(user = account.account)
        if len(twts) == 0:
            source_number = 0
        else:
            source_number = twts[0].followers

        data.append([account.account.encode("utf-8"), source_number])

    return data


