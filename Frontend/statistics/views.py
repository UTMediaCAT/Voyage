from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
from articles.models import *
from explorer.models import Msite
import sys, os, datetime, time, re
import analyzer

def articles(request):

    keywords_pie_chart = analyzer.keywords_pie_chart()
    articles_annotation_chart = analyzer.articles_annotation_chart()
    msites_bar_chart = analyzer.msites_bar_chart()

    context = {'keywords_pie_chart':  keywords_pie_chart, 'monitoring_sites': articles_annotation_chart[0], 'article_by_date': articles_annotation_chart[1], 'msites_bar_chart': msites_bar_chart,'msites_bar_table':msites_bar_chart[1:]}

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
