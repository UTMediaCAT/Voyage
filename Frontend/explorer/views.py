from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from subprocess import Popen
from explorer.models import Msite, Fsite, Keyword, Taccount
import sys, os, time, json

def command(request):
    if request.method == 'POST':
        if request.POST.get('acommand') == 'Run':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "article", "run"], cwd=path)

        if request.POST.get('acommand') == 'Pause':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "article", "pause"], cwd=path)

        if request.POST.get('acommand') == 'Stop':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "article", "stop"], cwd=path)

        if request.POST.get('acommand') == '[F]Stop':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "article", "fstop"], cwd=path)

        if request.POST.get('tcommand') == 'Run':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "twitter", "run"], cwd=path)

        if request.POST.get('tcommand') == 'Pause':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "twitter", "pause"], cwd=path)

        if request.POST.get('tcommand') == 'Stop':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "twitter", "stop"], cwd=path)

        if request.POST.get('tcommand') == '[F]Stop':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "twitter", "fstop"], cwd=path)


    return HttpResponseRedirect("/admin")

def getJson(request):
    scope = {'monitoring_sites':{}, 'foreign_sites': {}, 
             'keywords': [], 'twitter_accounts': []}

    for site in Msite.objects.all():
        scope['monitoring_sites'][site.url] = {'name': site.name}

    for site in Fsite.objects.all():
        scope['foreign_sites'][site.url] = {'name': site.name}

    for key in Keyword.objects.all():
        scope['keywords'].append(key.keyword)

    for acc in Taccount.objects.all():
        scope['twitter_accounts'].append(acc.account)

    res = HttpResponse(json.dumps(scope, indent=2, sort_keys=True))
    res['Content-Disposition'] = format('attachment; filename=scope-%s.json' 
                                        % time.strftime("%Y%m%d-%H%M%S"))
    return res
