from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
from articles.models import *
from explorer.models import *
import sys, os
import json

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'src'))
sys.path.append(path)
import visualizer

def coming_soon_Visuals(request):
    return render(request, 'visualizations/ComingSoon.html')