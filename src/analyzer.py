import django
import re
import operator
from articles.models import*
from articles.models import Keyword as ArticleKeyword
from articles.models import SourceSite as ArticleSourceSite
from explorer.models import*
from explorer.models import Keyword as ExplorerKeyword
from explorer.models import SourceSite as ExplorerSourceSite
from explorer.models import SourceTwitter as ExplorerSourceTwitter

from tweets.models import*
from tweets.models import Keyword as TwitterKeyword
import time

def articles_keywords_pie_chart():
    '''(None) -> list of list of [str, int]
    Search trough keywords table to count the number of times that each keywod is matched in articles.
    Return a list of list, where the inner list contains the name of keyword, and the number of matches.    
    '''
    data_dict = {}
    #get all keywords matched in the articles
    keywords = ArticleKeyword.objects.all()
    
    #loop trough the keywords
    for ele in keywords:
        #if the keyword hasn't been found yet,then add it to dict with count 1.
        if not ele.name in data_dict.keys():
            data_dict[ele.name] = 1
        else:
        #if it has been found, then add 1 to the count of the keywords.
            data_dict[ele.name] += 1
    #sort keywords by the number of count for each keyword
    sorted_data = sorted(data_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_data_dict = dict(sorted_data)
    
    #get top 10 keywrods based on the frequency of their occurrence
    if len(sorted_data)>10:
        sorted_data_dict = dict(sorted_data[0:10])
        sorted_data_dict_other = dict(sorted_data[10:])
        other_sum = sum (sorted_data_dict_other.values())
        sorted_data_dict["Other Keywords"] = other_sum

    #convert the dict to a list of list
    data = []

    for ele in sorted_data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(sorted_data_dict[ele])
        data.append(new)

    return data

def tweets_keywords_pie_chart():
    '''(None) -> list of list of [str, int]
    Search trough keywords table in database to count the number of times that each keywod is matched in tweets.
    Return a list of list, where the inner list contains the name of keyword, and the number of matches.    
    '''
    data_dict = {}
    #get all keywords matched in the tweet
    keywords = TwitterKeyword.objects.all()
    #loop trough the keywords   
    for ele in keywords:
        #if the keyword hasn't been found yet,then add it to dict with count 1.
        if not ele.name in data_dict.keys():
            data_dict[ele.name] = 1
        else:
        #if it has been found, then add 1 to the count of the keywords.
            data_dict[ele.name] += 1
    #sort keywords by the number of count for each keyword
    sorted_data = sorted(data_dict.items(), key=operator.itemgetter(1), reverse=True)

    sorted_data_dict = dict(sorted_data)
    #get top 10 keywrods based on the frequency of their occurrence
    if len(sorted_data)>10:
        sorted_data_dict = dict(sorted_data[0:10])
        sorted_data_dict_other = dict(sorted_data[10:])
        other_sum = sum (sorted_data_dict_other.values())
        sorted_data_dict["Other Keywords"] = other_sum

    #convert the dict to a list of list
    data = []

    for ele in sorted_data_dict.keys():
        new=[]
        new.append(ele.encode("utf-8"))
        new.append(sorted_data_dict[ele])
        data.append(new)

    return data

def articles_annotation_chart():
    '''(None) -> , lisr of str, list of list of [str, int] 
    Search trough article table in database to count the number of articles added on a particular day.
    Return a tuple where the first element is a list of names of monitoring sites, and the second element is 
    a list of list, where the inner list contains the name of keyword, and the number of matches.    
    '''
    #get all monitoring sites
    ReferringSites  = ReferringSite.objects.all()
    urls = []
    #loop through monitoring sites
    for element in ReferringSites:
        urls.append([element.url.encode("utf-8"), Article.objects.filter(url = element.url).count(), element.name.encode("utf-8")])
    
    #sort the monitoring sites by the number of articles they have.
    urls.sort(key = lambda x: x[1], reverse=True)
    #get top 10 monitoring sites based on the number of articles
    urls = urls[0:10]
    msites_name = []
    for a in range(len(urls)):
        msites_name.append(urls[a][2])

    for a in range(len(urls)):
        urls[a] = urls[a][0]

    data = []

    pre_date = None
    
    #loop through articles
    for art in Article.objects.all():
        new=[]
        #get day month, and year of each article
        date = art.date_added.strftime("%B %d, %Y")
        day = art.date_added.strftime("%d")
        month = art.date_added.strftime("%m")
        year = art.date_added.strftime("%Y")

        if date != pre_date:
            pre_date = date
            new.append(date)
            for url in urls:
                #count the number of articles added on that day, and add to the list.
                new.append(Article.objects.filter(domain = url, date_added__day = day, date_added__month = month, date_added__year = year).count())
            data.append(new)

    return msites_name, data

def msites_bar_chart():
    '''(None) -> list of list of [str, int]
    Search trough foreign site table in databse to count the number of articles used from each foreign site.  
    Return a list of list, where the inner list contains the name of foreign site, and the number of articles.    
    '''

    data = []
    #add the names of x-axis and y-axis for the bar chart.
    data.append (["Source Sites", "Number of Source Sites Matched"])

    #get all monitoring sites
    ssites = ExplorerSourceSite.objects.all()
    #loop through monitoring sites
    for site in ssites:
        source_number = ArticleSourceSite.objects.filter(domain = site.url).count()
        data.append([site.name.encode("utf-8"), source_number])
    #sort monitoring sites by the number of articles
        data.sort(key = lambda x: x[1], reverse=True)
    #only return the top 10 monitoring sites
    return data[0:11]

def tweets_annotation_chart():
    '''(None) -> , lisr of str, list of list of [str, int] 
    Search trough tweets table in database to count the number of tweets added on a particular day.
    Return a tuple where the first element is a list of names of monitoring sites, and the second element is 
    a list of list, where the inner list contains the name of keyword, and the number of matches.    
    '''
    #get all twitter accounts
    referringTwitter  = ReferringTwitter.objects.all()
    accounts = []
    #loop through twitter accounts
    for element in referringTwitter:
        accounts.append([element.name.encode("utf-8"), Tweet.objects.filter(name = element.name).count()])
    #sort the twitter accountsby the number of tweets they have.
    accounts.sort(key = lambda x: x[1], reverse=True)
    #get top 10 monitoring sites based on the number of tweets
    accounts = accounts[0:10]
    for a in range(len(accounts)):
        accounts[a] = accounts[a][0]


    data = []

    pre_date = None
    #loop through tweets
    for twt in Tweet.objects.all():
        new=[]
        #get day month, and year of each tweet
        date = twt.date_added.strftime("%B %d, %Y")
        day = twt.date_added.strftime("%d")
        month = twt.date_added.strftime("%m")
        year = twt.date_added.strftime("%Y")

        if date != pre_date:
            pre_date = date
            new.append(date)
            for account in accounts:
                #count the number of tweets added on that day, and add to the list.
                new.append(Tweet.objects.filter(name = account, date_added__day = day, date_added__month = month, date_added__year = year).count())
            data.append(new)

    return accounts, data
    
   
# For future implementation

'''
def follower_bar_chart():

    data = []
    data.append (["Source Sites","Number of source matched"])

    accounts = TwitterAccount.objects.all()
    for account in accounts:
        twts = Tweet.objects.filter(name = account.name)
        if not len(twts) == 0:
            source_number = twts[0].followers
        data.append([account.name.encode("utf-8"), source_number])
    data.sort(key = lambda x: x[1], reverse=True)

    return data[0:11]
    

def article_bubble_chart():
    data = []
    first = ['ID', 'Number of Keywords Matched', 'Number of Source Matched', 'Referring Sites']
    data.append(first)

    ReferringSites  = ReferringSite.objects.all()
    keywords = ExplorerKeyword.objects.all()
    fsites = SourceSite.objects.all()


    for msite in ReferringSites:
        new = []
        new.append(msite.name.encode("utf-8"))
        articles =  Article.objects.filter (domain = msite.url)
        count_keyword= 0
        count_source = 0
        for art in articles :
                count_keyword += ArticleKeyword.objects.filter(article = art).count()
                count_source += ArticleSource.objects.filter(article = art).count()

        new.append(count_keyword)
        new.append(count_source)
        new.append(msite.name.encode("utf-8"))


        data.append(new)

    return data

'''
