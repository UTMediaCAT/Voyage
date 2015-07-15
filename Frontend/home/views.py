from django.shortcuts import render, redirect
from django.template import RequestContext, loader

def index(request):
    return render(request, 'home/index.html')