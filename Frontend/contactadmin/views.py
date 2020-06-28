from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.

def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)
    return render(request, 'contactadmin/index.html')


def alert(request):
    messages.add_message(request, messages.INFO, 'Hello world.')
    return render(request, 'contactadmin/index.html')