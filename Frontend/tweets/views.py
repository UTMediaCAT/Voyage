from django.shortcuts import render, HttpResponse
from tweets.models import Tweet, Source, Keyword
import sys, os, time, json

# Create your views here.

def getJson(request):
    tweets = {}
    for twe in Tweet.objects.all():      
        tweets[twe.tweet_id] = {'text': twe.text, 'date_added': str(twe.date_added),
                             'date_published': str(twe.date_published),
                             'followers': twe.followers, 'matched_keywords': [],
                             'matched_sources': []}

    for key in Keyword.objects.all():
        tweets[key.tweet.tweet_id]['matched_keywords'].append(key.keyword)
    for src in Source.objects.all():
        tweets[src.tweet.tweet_id]['matched_sources'].append(src.source)

    res = HttpResponse(json.dumps(tweets, indent=2, sort_keys=True))
    res['Content-Disposition'] = format('attachment; filename=tweets-%s.json' 
                                        % time.strftime("%Y%m%d-%H%M%S"))
    return res
