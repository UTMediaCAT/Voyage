from django.shortcuts import render
from django.template import RequestContext, loader

from articles.models import Article


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