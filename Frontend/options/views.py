from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from subprocess import Popen
import sys, os

def downloads(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data = []

    context = {'data': data}
    return render(request, 'options/downloads.html', context)