from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
from articles.models import *
from explorer.models import Msite
import sys, os, datetime, time, re

def articles(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data_dict = {}

    keywords = Keyword.objects.all()
    for ele in keywords:
        if not ele.keyword in data_dict.keys():
            data_dict[ele.keyword] = 0
        else:
            data_dict[ele.keyword] +=1

    keyword_count = []
    for ele in data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(data_dict[ele])
        keyword_count.append(new)

    article_by_date = []
    sites = []
    for s in Msite.objects.all():
        sites.append(re.search("([a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.)+[a-zA-Z]{2,6}",
                     s.url, re.IGNORECASE).group(0).encode("ascii"))

    for art in Article.objects.all():
        added = False
        date = art.date_added.strftime("%Y-%m-%d")
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


    context = {'keyword_count': keyword_count, 'monitoring_sites': sites, 'article_by_date': article_by_date}


    return render(request, 'statistics/articles.html', context)

def tweets(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data_dict = {}

    keywords = Keyword.objects.all()
    for ele in keywords:
        if not ele.keyword in data_dict.keys():
            data_dict[ele.keyword] = 0
        else:
            data_dict[ele.keyword] +=1\

    data = []
    for ele in data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(data_dict[ele])
        data.append(new)

    context = {'data': data}
    return render(request, 'statistics/tweets.html', context)
