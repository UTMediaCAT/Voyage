from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
from articles.models import *
import sys, os

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

    data = []
    for ele in data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(data_dict[ele])
        data.append(new)

    context = {'data': data}
    return render(request, 'visualizations/articles.html', context)

def tweets(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data_dict = {}

    keywords = Keyword.objects.all()
    for ele in keywords:
        if not ele.keyword in data_dict.keys():
            data_dict[ele.keyword] = 0
        else:
            data_dict[ele.keyword] +=1

    data = []
    for ele in data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(data_dict[ele])
        data.append(new)

    context = {'data': data}
    return render(request, 'visualizations/tweets.html', context)
