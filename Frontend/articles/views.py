from django.shortcuts import render, HttpResponse
from django.template import RequestContext, loader
from articles.models import Article, Keyword, Source, Author
import sys, os, time, json

def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    latest_article_list = Article.objects.order_by('date_added')

    context = {'latest_article_list': latest_article_list}
    return render(request, 'articles/index.html', context)


def getJson(request):
    articles = {}
    for art in Article.objects.all():      
        articles[art.url] = {'title': art.title, 'date_added': str(art.date_added),
                             'date_published': str(art.date_published),
                             'influence': art.influence, 'matched_keywords': [],
                             'matched_sources': [], 'authors': []}

    for key in Keyword.objects.all():
        articles[key.article.url]['matched_keywords'].append(key.keyword)
    for src in Source.objects.all():
        articles[src.article.url]['matched_sources'].append(src.source)
    for ath in Author.objects.all():
        articles[ath.article.url]['authors'].append(ath.author)

    res = HttpResponse(json.dumps(articles, indent=2, sort_keys=True))
    res['Content-Disposition'] = format('attachment; filename=articles-%s.json' 
                                        % time.strftime("%Y%m%d-%H%M%S"))
    return res
