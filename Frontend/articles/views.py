from django.shortcuts import render, HttpResponse
from django.template import RequestContext, loader
from articles.models import Article, Keyword, Source, Author
import sys, os, time, json, yaml

def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    latest_article_list = Article.objects.order_by('date_added')

    context = {'latest_article_list': latest_article_list}
    return render(request, 'articles/index.html', context)


def getJson(request):
    articles = {}
    for art in Article.objects.all():      
        articles[art.url] = {'site': art.url_origin, 'title': art.title, 
                             'date_added': str(art.date_added),
                             'date_published': str(art.date_published),
                             'influence': art.influence, 'matched_keywords': [],
                             'matched_sources': [], 'authors': []}

    for key in Keyword.objects.all():
        articles[key.article.url]['matched_keywords'].append(key.keyword)
    for src in Source.objects.all():
        articles[src.article.url]['matched_sources'].append({'url':src.url, 
                                                             'site': src.url_origin})
    for ath in Author.objects.all():
        articles[ath.article.url]['authors'].append(ath.author)

    res = HttpResponse(json.dumps(articles, indent=4, sort_keys=True))
    res['Content-Disposition'] = format('attachment; filename=articles-%s.json' 
                                        % time.strftime("%Y%m%d-%H%M%S"))
    return res

def getWarc(request, filename):
    config = configuration()['warc']

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', config['dir'] + "/" + config['article_subdir']))
    filename_ext = path + "/" + filename + ".warc.gz"
    warc = open(filename_ext, "rb")
    res = HttpResponse(warc)
    warc.close()
    res['Content-Disposition'] = 'attachment; ' + filename + '.warc.gz'
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