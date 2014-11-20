from django.shortcuts import render, HttpResponse
from django.template import RequestContext, loader
from subprocess import Popen
from django.core.serializers import serialize
from articles.models import Article,Keyword, Source, Author
import sys, os, time

def index(request):
    latest_article_list = Article.objects.order_by('date_added')

    # output = ', '.join([p.title for p in latest_article_list])
    # return HttpResponse(output)


    # template = loader.get_template('articles/index.html')
    # context = RequestContext(request, {
    #     'latest_question_list': latest_article_list,
    # })
    # return HttpResponse(template.render(context))

    context = {'latest_article_list': latest_article_list}
    return render(request, 'articles/index.html', context)


def getJson(request):
    json = serialize('json', 
                     list(Article.objects.all()) + list(Keyword.objects.all()) + 
                     list(Source.objects.all()) + list(Author.objects.all()),
                     use_natural_foreign_keys=True, use_natural_primary_keys=True)
    res = HttpResponse(json)
    res['Content-Disposition'] = format('attachment; filename=articles-%s.json' 
                                        % time.strftime("%Y%m%d-%H%M%S"))
    return res
