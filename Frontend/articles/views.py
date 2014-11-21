from django.shortcuts import render
from django.template import RequestContext, loader
from subprocess import Popen
from articles.models import*
import sys, os




def index(request):
    
    data_dict = {}

    list = Keyword.objects.all()
    for ele in list:
        if not ele.keyword in data_dict.keys():
            data_dict[ele.keyword] = 0
        else:
            data_dict[ele.keyword] +=1
    print data_dict

    data = []
    for ele in data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(data_dict[ele])
        data.append(new)



    latest_article_list = Article.objects.order_by('date_added')
    

    # output = ', '.join([p.title for p in latest_article_list])
    # return HttpResponse(output)


    # template = loader.get_template('articles/index.html')
    # context = RequestContext(request, {
    #     'latest_question_list': latest_article_list,
    # })
    # return HttpResponse(template.render(context))

    context = {'latest_article_list': latest_article_list,'data': data}
    return render(request, 'articles/index.html', context)