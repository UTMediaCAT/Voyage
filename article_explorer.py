
import newspaper
from newspaper import news_pool
from newspaper import Article

#Testing imports
import timeit
import re


def populate_sites(sites, from_start):
    ''' Searches through the sites using newspaper library and
        returns list of sites with metadata

    Keyword arguments:
    sites -- List of [name, url] of each site
    from_start    -- Boolean to search sites from scratch
    '''

    new_sites = []
    for s in range(len(sites)):
        # Duplicate the name of the sites
        new_sites.append([sites[s][0]])

        # Use the url and build the metadata of the sites
        new_sites[s].append((newspaper.build(sites[s][1],
                                             memoize_articles=not from_start)))

    return new_sites

def download_articles(populated_sites, thread_per_source):
    ''' Download all articles from built sites with number of threads to use

    Keyword arguments:
    populated_sites -- List of [name, 'built_article'] of each site
    total_threads   -- Number of threads to use for downloading per sites.
                       This can greatly increase the speed of download
    '''
    for site in populated_sites:
        for art in site[1].articles:
            art.download()
            art.parse()
            art.source_url    # can be used for site i.e. cnn.com
            art.authors       # author    Done
            art.title         # title     Done
            art.meta_data     # date      IP
            art.url           # url       Done
            art.text          # keyword   IP
            get_sources()               # sources   Done


def get_sources(article):
    sc, sp, ep = 20, 0, 0
    html = re.sub('<[^((a|link).*?href)].*?>', ".", first_article.html)

    start = first_article.text[:sc]
    end = first_article.text[-sc:]
    start = re.sub("[^0-9a-zA-Z ]+", ".", start)
    end = re.sub("[^0-9a-zA-Z ]+", ".", end)

    while ("." in start):
        start = first_article.text[sp:sc+sp]
        start = re.sub("[^0-9a-zA-Z ]+", ".*?", start)
        sp+=1

    while ("." in end):
        end = first_article.text[-(ep+sc):min(-ep, -1)]
        end = re.sub("[^0-9a-zA-Z ]+", ".*?", end)
        ep+=1

    print "FS: %2i - '%s'\nES: %2i - '%s'"%(sp, start, ep, end)
    regex = "(?=(" + start + ".*?" + end + "))"
    text_html =  min(re.findall(regex, html, re.DOTALL), key=len)
    urls = re.findall("href=[\"\'].*?[\"\']", text_html)
    for i in range(len(urls) - 1):
        urls[i] = urls[i][6:-1]
    return urls
    # regex = article.text[10:30] + '.*?' + article.text[-30:-10]
    # regex = re.sub("[^0-9a-zA-Z ]+", ".*?", regex)
    # if regex[:3] == ".*?":
    #     regex = regex[3:]
    # if regex[-3:] == ".*?":
    #     regex = regex[:-3]
    # regex = "(?=(" + regex + "))"
    # text_html =  min(re.findall(regex, article.html, re.DOTALL), len)
    # urls = re.findall("href=[\"\'].*?[\"\']",text_html)
    # for i in range(len(urls) - 1):
    #     urls[i] = urls[i][4:-1]

# def find_artciles(allMonitoredSites):
#     pass
#     #forloop(monitored sites):
#         #SitesToArticles(Name, foreignSites):
#             #article tp ward
#             #war to db
#     #return None

if __name__ == '__main__':
    # a = [['cnn', 'http://cnn.com'], ['nyt', 'http://nytimes.com']]
    # a = [['cnn', 'http://cnn.com']]
    # start = timeit.default_timer()
    # b = populate_sites(a, False)
    # stop = timeit.default_timer()
    # print stop - start
    # for art in b[0][1].articles:
    #     start = timeit.default_timer()
    #     art.download()
    #     art.parse()
    #     print art.title
    #     print art.meta_data
    #     if art.meta_data['pubdate'] == {}:
    #         print art.meta_data['date']
    #     else:
    #         print art.meta_data['pubdate']
    #     print art.meta_data['author']
    #
    #     stop = timeit.default_timer()
    #     print stop - start
    #
    #     print("")
    #
    # stop = timeit.default_timer()
    # print stop - start
    # start = timeit.default_timer()
    #
    # c = download_articles(b, 10)
    # stop = timeit.default_timer()
    # print stop - start



    # from newspaper import Article
    # urls = ["http://www.cnn.com/2014/10/12/living/columbus-day-indigenous-people-day/index.html?hpt=hp_t2",
    #         "http://www.cnn.com/2014/10/12/health/ebola/index.html?hpt=hp_t1",
    #         "http://www.cnn.com/2014/10/10/health/sperm-donor-qa/index.html?hpt=hp_c2",
    #         "http://www.nytimes.com/2014/10/13/world/asia/once-a-symbol-of-power-farming-now-an-economic-drag-in-china.html?hp&action=click&pgtype=Homepage&version=LargeMediaHeadlineSum&module=photo-spot-region&region=top-news&WT.nav=top-news&_r=0",
    #         "http://www.cbc.ca/news/canada/calgary/downtown-calgary-electrical-fire-damage-will-take-days-to-rebuild-1.2796497"]
    # for url in urls:
    #     start = timeit.default_timer()
    #     first_article = Article(url)
    #     first_article.download()
    #     first_article.parse()
    #
    #     print first_article.title
    #
    #     html = re.sub('<[^((a|link).*?href)].*?>', ".", first_article.html)
    #     sc = 20
    #
    #     start = first_article.text[:sc]
    #     end = first_article.text[-sc:]
    #     start = re.sub("[^0-9a-zA-Z ]+", ".", start)
    #     end = re.sub("[^0-9a-zA-Z ]+", ".", end)
    #
    #     sp, ep = 0, 0
    #     while ("." in start):
    #         start = first_article.text[sp:sc+sp]
    #         start = re.sub("[^0-9a-zA-Z ]+", ".*?", start)
    #         sp+=1
    #     while ("." in end):
    #         end = first_article.text[-(ep+sc):min(-ep, -1)]
    #         end = re.sub("[^0-9a-zA-Z ]+", ".*?", end)
    #         ep+=1
    #     print "FS: %2i - '%s'\nES: %2i - '%s'"%(sp, start, ep, end)
    #     regex = "(?=(" + start + ".*?" + end + "))"
    #     text_html =  min(re.findall(regex, html, re.DOTALL), key=len)
    #     urls = re.findall("href=[\"\'].*?[\"\']", text_html)
    #     for i in range(len(urls) - 1):
    #         urls[i] = urls[i][6:-1]
    #     print urls
    #     print len(urls)
    #     print ""

    pass