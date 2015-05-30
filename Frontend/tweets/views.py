from django.shortcuts import render, HttpResponse
from tweets.models import Tweet, Source, Keyword
import sys, os, time, json, yaml, urllib

# Create your views here.

def getJson(request):
    tweets = {}
    for twe in Tweet.objects.all():      
        tweets[twe.tweet_id] = {'text': twe.text, 'date_added': str(twe.date_added),
                             'date_published': str(twe.date_published),
                             'matched_keywords': [], 'matched_sources': []}

    for key in Keyword.objects.all():
        tweets[key.tweet.tweet_id]['matched_keywords'].append(key.name)
    for src in Source.objects.all():
        tweets[src.tweet.tweet_id]['matched_sources'].append({'url':src.url, 
                                                             'url_site': src.domain})

    res = HttpResponse(json.dumps(tweets, indent=2, sort_keys=True))
    res['Content-Disposition'] = format('attachment; filename=tweets-%s.json' 
                                        % time.strftime("%Y%m%d-%H%M%S"))
    return res

def getWarc(request, filename):
    config = configuration()['warc']

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', config['dir'] + "/" + config['twitter_subdir']))
    filename_ext = path + "/" + filename + ".warc.gz"
    warc = open(filename_ext, "rb")
    res = HttpResponse(warc, content_type="application/force-download")
    warc.close()

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % (filename + '.warc.gz').encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote((filename + '.warc.gz').encode('utf-8'))
    res['Content-Disposition'] = 'attachment; ' + filename_header

    return res

def configuration():
    """ (None) -> dict
    Returns a dictionary containing the micro settings from the
    config.yaml file located in the directory containing this file
    """
    config_yaml = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../',"config.yaml")), 'r')
    config = yaml.load(config_yaml)
    config_yaml.close()
    return config
