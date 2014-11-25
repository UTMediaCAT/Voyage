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

def article_spacetree(site):
    data = []
    if site == None:
        msites = Msite.objects.all()
    else:
        msites = Msite.objects.filter(name = site)

    for msite in msites:
        site_data = {}
        site_data["id"] = msite.url
        site_data["name"] = msite.name
        site_data["children"] = []
        site_data["data"] = {"relation": "Sourced"}

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
            site_data["children"].append(keywords_data)

        data.append(site_data)

    if site == None:
        data = {"id": "Msites", "name": "Monitoring Sites", "children": data, "relation": "Monitoring Sites"}
    else:
        if len(data) != 0:
            data = data[0]
        else:
            data = []

    return data, Msite.objects.all()

def article_weightedtree(site):
    msites = []
    max_dim = 0

    if site == None:
        results = Msite.objects.all()
    else:
        results = Msite.objects.filter(name = site)

    for msite in results:
        data = {}
        data["id"] = msite.url
        data["name"] = msite.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        fsites_dict = {}
        for article in Article.objects.filter(url_origin = msite.url):
            keywords = A_Keyword.objects.filter(article = article)
            fsites = A_Source.objects.filter(article = article)

            for keyword in keywords:
                if keyword.keyword in keywords_dict.keys():
                    keywords_dict[keyword.keyword].append(keyword)
                else:
                    keywords_dict[keyword.keyword] = [keyword]

            for fsite in fsites:
                if fsite.url_origin in fsites_dict.keys():
                    fsites_dict[fsite.url_origin].append(fsite)
                else:
                    fsites_dict[fsite.url_origin] = [fsite] 
                
        for keyword in keywords_dict.keys():
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["nodeTo"] = keyword

            data["adjacencies"].append(keywords_data)
            data["data"]["$dim"] += len(keywords_dict[keyword])
            keywords_data_info = keywords_data.copy()
            keywords_data_info["data"] = {"$dim": len(keywords_dict[keyword]), "$type": "square", "$color": "#00AA00"}
            msites.append(keywords_data_info)

        for fsite in fsites_dict.keys():
            fsites_data = {}
            fsites_data["id"] = fsite
            fsites_data["name"] = fsite
            fsites_data["nodeTo"] = fsite

            data["adjacencies"].append(fsites_data)
            data["data"]["$dim"] += len(fsites_dict[fsite])
            fsites_data_info = fsites_data.copy()
            fsites_data_info["data"] = {"$dim": len(fsites_dict[fsite]), "$type": "circle", "$color": "#FF0000"}
            msites.append(fsites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        msites.append(data)

    for msite in msites:
        msite["data"]["$dim"] = int(msite["data"]["$dim"] * 30.0 / max_dim) + 10

    return msites, Msite.objects.all()

def article_forcegraph(site):
    msites = []
    max_dim = 0

    if site == None:
        results = Msite.objects.all()
    else:
        results = Msite.objects.filter(name = site)

    for msite in results:
        data = {}
        data["id"] = msite.url
        data["name"] = msite.name
        data["adjacencies"] = []
        data["data"] = {"$dim": 0, "$type": "triangle", "$color": "#0000FF"}

        keywords_dict = {}
        fsites_dict = {}
        for article in Article.objects.filter(url_origin = msite.url):
            keywords = A_Keyword.objects.filter(article = article)
            fsites = A_Source.objects.filter(article = article)

            for keyword in keywords:
                if keyword.keyword in keywords_dict.keys():
                    keywords_dict[keyword.keyword].append(keyword)
                else:
                    keywords_dict[keyword.keyword] = [keyword]

            for fsite in fsites:
                if fsite.url_origin in fsites_dict.keys():
                    fsites_dict[fsite.url_origin].append(fsite)
                else:
                    fsites_dict[fsite.url_origin] = [fsite] 
                
        for keyword in keywords_dict.keys():
            keywords_data = {}
            keywords_data["id"] = keyword
            keywords_data["name"] = keyword
            keywords_data["nodeTo"] = keyword
            keywords_data["data"] = {"$weight": len(keywords_dict[keyword])}

            data["adjacencies"].append(keywords_data)
            data["data"]["$dim"] += len(keywords_dict[keyword])
            keywords_data_info = keywords_data.copy()
            keywords_data_info["data"] = {"$dim": len(keywords_dict[keyword]), "$type": "square", "$color": "#00AA00"}
            msites.append(keywords_data_info)

        for fsite in fsites_dict.keys():
            fsites_data = {}
            fsites_data["id"] = fsite
            fsites_data["name"] = fsite
            fsites_data["nodeTo"] = fsite
            fsites_data["data"] = {"$weight": len(fsites_dict[fsite])}

            data["adjacencies"].append(fsites_data)
            data["data"]["$dim"] += len(fsites_dict[fsite])
            fsites_data_info = fsites_data.copy()
            fsites_data_info["data"] = {"$dim": len(fsites_dict[fsite]), "$type": "circle", "$color": "#FF0000"}
            msites.append(fsites_data_info)

        max_dim = max(data["data"]["$dim"], max_dim)
        msites.append(data)

    for msite in msites:
        msite["data"]["$dim"] = int(msite["data"]["$dim"] * 30.0 / max_dim) + 10
        if "adjacencies" in msite.keys():
            for ele in msite["adjacencies"]:
                ele["data"]["$weight"] = int(ele["data"]["$weight"] * 30.0 / max_dim) + 10

    return msites, Msite.objects.all()

def tweet_hypertree():
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

def tweet_spacetree():
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

def tweet_weightedtree():
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

def tweet_forcegraph():
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)
