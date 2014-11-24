import django
import re



from articles.models import*
from articles.models import Keyword as A_Keyword
from explorer.models import *
from explorer.models import Keyword as E_Keyword



def keywords_pie_chart():
    data_dict = {}

    keywords = A_Keyword.objects.all()
    for ele in keywords:
        if not ele.keyword in data_dict.keys():
            data_dict[ele.keyword] = 1
        else:
            data_dict[ele.keyword] += 1

    data = []
    for ele in data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(data_dict[ele])
        data.append(new)

    return data

def articles_annotation_chart():
    article_by_date = []
    sites = []
    for s in Msite.objects.all():
        sites.append(re.search("([a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.)+[a-zA-Z]{2,6}",
                     s.url, re.IGNORECASE).group(0).encode("ascii"))

    for art in Article.objects.all():
        added = False
        date = art.date_added.strftime("%B %d, %Y")
        for index in range(len(article_by_date)):
            if date == article_by_date[index][0]:
                added = True
                for i in range(len(sites)):
                    if sites[i] in art.url.encode("ascii"):
                        article_by_date[index][i+1] += 1
                        break
            if added:
                break

        if not added:
            article_by_date.append([date] + [0]*len(sites))
            for i in range(len(sites)):
                if sites[i] in art.url:
                    article_by_date[-1][i+1] += 1
                    break
    return sites, article_by_date


def msites_bar_chart():

    data = []
    data.append (["foreign sites","Number of source matched"])

    fsites = Fsite.objects.all()
    for site in fsites:
        source_number = Source.objects.filter(url_origin = site.url).count()
        print source_number
        data.append([site.name.encode("utf-8"),source_number])

    return data







