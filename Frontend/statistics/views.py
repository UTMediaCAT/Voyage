from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
import sys, os, datetime, time, re

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'src'))
sys.path.append(path)
import analyzer
import Caching

def articles(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data = []
    context = {'data': data}
    return render(request, 'statistics/articles.html', context)

def articles_js(request):
    data = Caching.getCacheData("Article_Statistics.Json")
    #print data
    return render(request, 'statistics/articles_js.html', data)

def tweets(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data = []
    context = {'data': data}
    return render(request, 'statistics/tweets.html', context)

def tweets_js(request):
    data = Caching.getCacheData("Tweet_Statistics.Json")
    #print data
    return render(request, 'statistics/tweets_js.html', data)
