from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
import sys, os, datetime, time, re

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'src'))
sys.path.append(path)
import analyzer
import Caching

def coming_soon_statistics(request):
    #print data
    return render(request, 'statistics/coming_soon.html')
