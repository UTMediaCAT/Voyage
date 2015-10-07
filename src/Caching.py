__author__ = 'wangx173'

import analyzer
import json
import visualizer

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def setArticleCachedData():
        keywords_pie_chart =  analyzer.articles_keywords_pie_chart()
        articles_annotation_chart =  analyzer.articles_annotation_chart()
        msites_bar_chart =   analyzer.msites_bar_chart()

        with open("Article_Statistics.Json", 'w') as outfile:

            context = {'keywords_pie_chart':  keywords_pie_chart,
            'referring_sites': articles_annotation_chart[0],
            'article_by_date': articles_annotation_chart[1],
            'referringsite_bar_chart': msites_bar_chart,
            'referringsite_bar_table':msites_bar_chart[1:],
            'bar_chart_height': max((len(msites_bar_chart) - 1) * 3, 30),}


            json.dump(context, outfile)



def setTweetCachedData():

        keywords_pie_chart =  analyzer.tweets_keywords_pie_chart()
        tweets_annotation_chart =  analyzer.tweets_annotation_chart()

        with open("Tweet_Statistics.Json", 'w') as outfile:

            context = {'keywords_pie_chart': keywords_pie_chart,
                        'referring_acounts':tweets_annotation_chart[0],
                        'tweet_by_date': tweets_annotation_chart[1]}

            json.dump(context, outfile)



#Cacheing for visualization




def set_visualization(name,data):

    with open(name, 'w') as outfile:
        json.dump(data, outfile)

    outfile.close()







#getting cached data

def getCacheData(name):

    with open(name) as json_file:
        json_data = json.load(json_file)
    json_file.close()
    return byteify(json_data)










'''
    with open('profile_log', 'rb') as profile_log:
        reader = csv.reader(profile_log)
        for row in reader:
            if(len(row) == 1):
                if(row[0].startswith("site: ")):
                    current = []
                    print row[0][6:]
                    result[row[0][5:]] = current
            elif(len(row) >= 4 and len(row) <= 7):
                crawler_download = row[0]
                crawler_parse = row[1]
                crawler_total = row[2]
                article_parse = ""
                article_db = ""
                article_warc = ""
                article_total = row[-1]
                if(len(row) >= 5):
                    article_parse = row[3]
                if(len(row) == 7):
                    article_db = row[4]
                    article_warc = row[5]


                current.append({"crawler_download":crawler_download,
                                "crawler_parse": crawler_parse,
                                "crawler_total": crawler_total,
                                "article_parse":article_parse,
                                "article_db":article_db,
                                "article_warc":article_warc,
                                "article_total":article_total})
            else:
                print
'''
