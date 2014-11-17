from django.http import HttpResponseRedirect
from subprocess import Popen
import sys, os

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

        if request.POST.get('tcommand') == 'Run':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "twitter", "run"], cwd=path)

        if request.POST.get('tcommand') == 'Pause':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "twitter", "pause"], cwd=path)

        if request.POST.get('tcommand') == 'Stop':
            path = os.path.dirname(os.path.realpath(__file__))
            Popen(["python", path + "/../../src/executer.py", "twitter", "stop"], cwd=path)


    return HttpResponseRedirect("/admin")