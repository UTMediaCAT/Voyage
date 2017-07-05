from django.shortcuts import render, redirect
from django.template import RequestContext, loader


def notAvailable(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    return render(request, 'statistics/notAvailable.html')
