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
import time

def articles_keywords_pie_chart():
    data_dict = {}
    
    keywords = A_Keyword.objects.all()

    for ele in keywords:
        if not ele.keyword in data_dict.keys():
            data_dict[ele.keyword] = 1
        else:
            data_dict[ele.keyword] += 1
    sorted_data = sorted(data_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_data_dict = dict(sorted_data)

    if len(sorted_data)>5:
        sorted_data_dict = dict(sorted_data[0:5])
        sorted_data_dict_other = dict(sorted_data[5:])
        other_sum = sum (sorted_data_dict_other.values())
        sorted_data_dict["Other Keywrods"] = other_sum


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
    sorted_data = sorted(data_dict.items(), key=operator.itemgetter(1), reverse=True)

    sorted_data_dict = dict(sorted_data)

    if len(sorted_data)>10:
        sorted_data_dict = dict(sorted_data[0:10])
        sorted_data_dict_other = dict(sorted_data[10:])
        other_sum = sum (sorted_data_dict_other.values())
        sorted_data_dict["Other Keywrods"] = other_sum


    data = []

    for ele in sorted_data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(sorted_data_dict[ele])
        data.append(new)

    return data

def articles_annotation_chart():

    Msites  = Msite.objects.all()
    urls = []
    for element in Msites:
        urls.append([element.url.encode("utf-8"), Article.objects.filter(url = element.url).count(), element.name.encode("utf-8")])

    urls.sort(key = lambda x: x[1], reverse=True)
    urls = urls[0:10]
    msites_name = []
    for a in range(len(urls)):
        msites_name.append(urls[a][2])

    for a in range(len(urls)):
        urls[a] = urls[a][0]




    data = []

    pre_date = None
    
    for art in Article.objects.all():
        new=[]
        date = art.date_added.strftime("%B %d, %Y")
        day = art.date_added.strftime("%d")
        month = art.date_added.strftime("%m")
        year = art.date_added.strftime("%Y")

        if date != pre_date:
            pre_date = date
            new.append(date)
            for url in urls:
                new.append(Article.objects.filter(url_origin = url, date_added__day = day, date_added__month = month, date_added__year = year).count())
            data.append(new)

    return msites_name, data

def msites_bar_chart():

    data = []
    data.append (["Foreign Sites", "Number of source matched"])


    fsites = Fsite.objects.all()
    for site in fsites:
        source_number = A_Source.objects.filter(url_origin = site.url).count()
        data.append([site.name.encode("utf-8"), source_number])
    data.sort(key = lambda x: x[1], reverse=True)

    return data[0:11]

def tweets_annotation_chart():

    Taccounts  = Taccount.objects.all()
    accounts = []
    for element in Taccounts:
        accounts.append([element.account.encode("utf-8"), Tweet.objects.filter(user = element.account).count()])

    accounts.sort(key = lambda x: x[1], reverse=True)
    accounts = accounts[0:10]
    for a in range(len(accounts)):
        accounts[a] = accounts[a][0]


    data = []

    pre_date = None
    
    for twt in Tweet.objects.all():
        new=[]
        date = twt.date_added.strftime("%B %d, %Y")
        day = twt.date_added.strftime("%d")
        month = twt.date_added.strftime("%m")
        year = twt.date_added.strftime("%Y")

        if date != pre_date:
            pre_date = date
            new.append(date)
            for account in accounts:
                new.append(Tweet.objects.filter(user = account, date_added__day = day, date_added__month = month, date_added__year = year).count())
            data.append(new)

    return accounts, data

def follower_bar_chart():

    data = []
    data.append (["Foreign Sites","Number of source matched"])

    accounts = Taccount.objects.all()
    for account in accounts:
        twts = Tweet.objects.filter(user = account.account)
        if not len(twts) == 0:
            source_number = twts[0].followers
        data.append([account.account.encode("utf-8"), source_number])
    data.sort(key = lambda x: x[1], reverse=True)

    return data[0:11]
    

def article_bubble_chart():
    start = time.clock()
    data = []
    first = ['ID', 'Number of Keywords Matched', 'Number of Source Matched', 'Monitoring Sites']
    data.append(first)

    Msites  = Msite.objects.all()
    keywords = E_Keyword.objects.all()
    fsites = Fsite.objects.all()


    for msite in Msites:
        new = []
        new.append(msite.name.encode("utf-8"))
        articles =  Article.objects.filter (url_origin = msite.url)
        count_keyword= 0
        count_source = 0
        for art in articles :
                count_keyword += A_Keyword.objects.filter(article = art).count()
                count_source += A_Source.objects.filter(article = art).count()

        new.append(count_keyword)
        new.append(count_source)
        new.append(msite.name.encode("utf-8"))


        data.append(new)
    print time.clock() - start

    return data

