from django.shortcuts import render, redirect
from django.template import RequestContext, loader

def not_available(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    return render(request, 'visualizations/notAvailable.html')
