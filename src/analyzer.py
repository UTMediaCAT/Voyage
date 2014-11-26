import django
import re
import operator
from articles.models import*
from articles.models import Keyword as A_Keyword
from articles.models import Source as A_Source
from explorer.models import*
from explorer.models import Keyword as E_Keyword
from tweets.models import*
from tweets.models import Keyword as T_Keyword

def articles_keywords_pie_chart():
    data_dict = {}
    
    keywords = A_Keyword.objects.all()

    count = 0
    for ele in keywords:
        if not ele.keyword in data_dict.keys():
            data_dict[ele.keyword] = 1
        else:
            data_dict[ele.keyword] += 1
    sorted_data = sorted(data_dict.items(), key=operator.itemgetter(1), reverse=True)
    print sorted_data
    sorted_data_dict = dict(sorted_data)

    if len(sorted_data)>10:
        sorted_data_dict = dict(sorted_data[10:])
        sorted_data_dict_other = sorted_data[10:]
        other_sum = sum (sorted_data_dict_other.values())
        sorted_data_dict["other"] = other_sum


    data = []

    for ele in sorted_data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(sorted_data_dict[ele])
        data.append(new)

    return data

def tweets_keywords_pie_chart():
    data_dict = {}
     
    keywords = T_Keyword.objects.all()
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
    data.append (["Foreign Sites", "Number of source matched"])


    fsites = Fsite.objects.all()
    for site in fsites:
        source_number = A_Source.objects.filter(url_origin = site.url).count()
        data.append([site.name.encode("utf-8"), source_number])
    return data




def tweets_annotation_chart():
    Taccounts  = Taccount.objects.all()
    accounts = []
    for element in Taccounts:
        accounts.append(element.account.encode("utf-8"))

    data = []

    pre_date = None

    for twt in Tweet.objects.all():
        new=[]
        date = twt.date_added.strftime("%B %d, %Y")
        if date == pre_date:
            break;
        else:
            pre_date = date
            new.append(date)
            for account in accounts:
                new.append(Tweet.objects.filter(date_added = twt.date_added).count())
            data.append(new)
    return accounts, data


def follower_bar_chart():

    data = []
    data.append (["Foreign Sites","Number of source matched"])

    accounts = Taccount.objects.all()
    for account in accounts:
        twts = Tweet.objects.filter(user = account.account)
        if len(twts) == 0:
            source_number = 0
        else:
            source_number = twts[0].followers

        data.append([account.account.encode("utf-8"), source_number])

    return data


