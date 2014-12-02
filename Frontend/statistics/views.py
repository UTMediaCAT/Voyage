from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
import sys, os, datetime, time, re

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'src'))
sys.path.append(path)
import analyzer

def articles(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    keywords_pie_chart = analyzer.articles_keywords_pie_chart()
    articles_annotation_chart = analyzer.articles_annotation_chart()
    msites_bar_chart = analyzer.msites_bar_chart()


    context = {'keywords_pie_chart':  keywords_pie_chart, 
                'monitoring_sites': articles_annotation_chart[0], 
                'article_by_date': articles_annotation_chart[1], 
                'msites_bar_chart': msites_bar_chart,
                'msites_bar_table':msites_bar_chart[1:],
                'bar_chart_height': max((len(msites_bar_chart) - 1) * 3, 30),}

    return render(request, 'statistics/articles.html', context)

def tweets(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    keywords_pie_chart = analyzer.tweets_keywords_pie_chart()
    tweets_annotation_chart =analyzer.tweets_annotation_chart()



    context = {'keywords_pie_chart': keywords_pie_chart, 
                'monitoring_acounts':tweets_annotation_chart[0], 
                'tweet_by_date': tweets_annotation_chart[1]}
    return render(request, 'statistics/tweets.html', context)
