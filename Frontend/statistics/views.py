from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
from articles.models import *
from explorer.models import Msite
import sys, os, datetime, time, re
import analyzer

def articles(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    keywords_pie_chart = analyzer.keywords_pie_chart(True)
    articles_annotation_chart = analyzer.articles_annotation_chart()
    msites_bar_chart = analyzer.msites_bar_chart()

    context = {'keywords_pie_chart':  keywords_pie_chart, 'monitoring_sites': articles_annotation_chart[0], 'article_by_date': articles_annotation_chart[1], 'msites_bar_chart': msites_bar_chart,'msites_bar_table':msites_bar_chart[1:]}

    return render(request, 'statistics/articles.html', context)

def tweets(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    keywords_pie_chart = analyzer.keywords_pie_chart(False)
    tweets_annotation_chart =analyzer.tweets_annotation_chart()
    follower_bar_chart = analyzer.follower_bar_chart()


    context = {'keywords_pie_chart': keywords_pie_chart, 'monitoring_acounts':tweets_annotation_chart[0], 'tweet_by_date': tweets_annotation_chart[1],'follower_bar_chart':follower_bar_chart,'follower_bar_table':follower_bar_chart[1:]}
    return render(request, 'statistics/tweets.html', context)
