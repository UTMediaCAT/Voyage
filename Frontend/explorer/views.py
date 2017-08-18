from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from subprocess import Popen
from explorer.models import (
    ReferringSite,
    ReferringSiteFilter,
    ReferringSiteCssSelector,
    ReferringTwitter,
    SourceTwitter,
    SourceTwitterAlias,
    SourceSite,
    SourceSiteAlias,
    Keyword
)
import sys, os, time, json
from taggit.models import TaggedItem

from django.core import serializers, management
from StringIO import StringIO

import newspaper
import common

def validate_site(site):
    try:
        s = newspaper.build(site, memoize_articles=False,
                            keep_article_html=True,
                            fetch_images=False,
                            language='en')
        return HttpResponse(format('%s articles found using RSS Scan!' % s.size()))
    except:
        return HttpResponse(format('%s is not a valid Referring Site!' % site))

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

        if request.POST.get('url'):
        	return validate_site(request.POST.get('url'))

        if request.POST.get('referring'):
            referring = request.POST.get('referring')
            for site in SourceSite.objects.all():
                if site.url == referring:
                    return HttpResponse(format('%s exists in Source Sites Scope.' % referring))
            return HttpResponse(format('%s does not exist in Source Sites Scope.' % referring))

    return HttpResponseRedirect("/admin")

def getJson(request):
    scope = {
        'name': 'mediacat-scope',
        'version': common.get_config()['database']['version'],
        'date': time.strftime("%c"),
    }

    json_serializer = serializers.get_serializer('json')()

    scope['referring_sites'] = json.loads(json_serializer.serialize(ReferringSite.objects.all()))
    scope['referring_sites_filter'] = json.loads(json_serializer.serialize(ReferringSiteFilter.objects.all()))
    scope['referring_sites_css_selector'] = json.loads(json_serializer.serialize(ReferringSiteCssSelector.objects.all()))
    scope['referring_twitter'] = json.loads(json_serializer.serialize(ReferringTwitter.objects.all()))
    scope['source_twitter'] = json.loads(json_serializer.serialize(SourceTwitter.objects.all()))
    scope['source_twitter_alias'] = json.loads(json_serializer.serialize(SourceTwitterAlias.objects.all()))
    scope['source_sites'] = json.loads(json_serializer.serialize(SourceSite.objects.all()))
    scope['source_sites_alias'] = json.loads(json_serializer.serialize(SourceSiteAlias.objects.all()))
    scope['keywords'] = json.loads(json_serializer.serialize(Keyword.objects.all()))
    scope['taggit'] = json.loads(json_serializer.serialize(TaggedItem.objects.all()))

    res = HttpResponse(json.dumps(scope, indent=2, sort_keys=True))
    res['Content-Disposition'] = format('attachment; filename=scope-%s.json' 
                                        % time.strftime("%Y%m%d-%H%M%S"))
    return res

def getDump(request):
    version = common.get_config()['database']['version']
    out = StringIO()
    management.call_command('dumpdata', 'explorer', 'taggit', stdout=out)
    res = HttpResponse(version + '\n' + out.getvalue())
    res['Content-Disposition'] = format('attachment; filename=scope-%s.json' 
                                        % time.strftime("%Y%m%d-%H%M%S"))
    return res
