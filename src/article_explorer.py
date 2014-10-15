
# newspaper
import newspaper
from newspaper import news_pool
from newspaper import Article
import lxml.html.clean

#regex
import re

#Times
import timeit
import time
#dateutil
from dateutil import parser

#db_manager
import db_manager as db



def populate_sites(sites, from_start):
    ''' (list of str, bool) -> dict of str:Newspaper
    Searches through the sites using newspaper library and
    returns list of sites with available articles populated

    Keyword arguments:
    sites         -- List of [name, url] of each site
    from_start    -- Boolean to search sites from scratch
    '''

    new_sites = []
    for s in range(len(sites)):
        start = time.time()
        # Duplicate the name of the sites
        new_sites.append([sites[s][0]])

        # Use the url and build the metadata of the sites
        new_sites[s].append((newspaper.build(sites[s][1],
                                             memoize_articles=not from_start,
                                             keep_article_html=True)))
        end = time.time()
        print ("Populated: %-5s Found: %5i pages in %is"%(sites[s][0], new_sites[s][1].size(), end - start))

    return new_sites

def download_articles(populated_sites, db_keywords, foreign_sites, db_name):
    ''' (dict of str:newspaper.source.Source, list of str, list of str, str) -> None
    Download all articles from built sites and stores the metadata
    to the database

    Keyword arguments:
    populated_sites -- List of [name, 'built_article'] of each site
    total_threads   -- Number of threads to use for downloading per sites.
                       This can greatly increase the speed of download
    '''
    added, failed,no_match = 0,0,0
    start = time.time()

    db.connect(db_name)

    for site in populated_sites:
        for art in site[1].articles:
            try:
                art.download()
                art.parse()
                title = art.title                                 # title     Done
            except:
                title == ""


            print "Title:    ", title

            if not ((title == "") or (title == "Page not found")):
                keywords = get_keywords(art, db_keywords)
                sources = get_sources(art.article_html, foreign_sites)
                if not (keywords == [] and sources == []):
                    url =  art.url                                   # url       Done
                    authors = art.authors                               # author    Done
                    date = get_date(art)                             # date      Done

                    print "Site:     ", site[0]
                    print "URL:      ", url
                    print "Author:   ", authors
                    print "Date:     ", date
                    print "Keywords: ", keywords
                    print "Sources:  ", sources
                    # db.add_document({"_id":url, "title":title, "date":date, "author":authors, "sources":sources})

                    added += 1
                else:
                    print "URL:      ", art.url
                    print "\nFailed: No Site nor Keyword matched."
                    no_match += 1
            else:
                print "URL:      ", art.url
                print "\nFailed: Page was not able to download"
                failed += 1

            print ("\nAdded: %8i\nFailed: %7i\nNo Match; %5i"%(added,failed,no_match))
            print ("%is"%(time.time() - start))
            print ("\n=============================================================================================\n")


def get_sources(html, sites):
    ''' (str, list of str) -> list of str
    Searches and returns links redirected to sites within the html
    Returns empty list if none found

    Keyword arguments:
    html            -- string of html
    sites           -- List of site urls to look for
    '''
    matched_urls = []

    for site in sites:
        for url in re.findall("href=[\"\'][^\"\']*?" + re.escape(site) + "[^\"\']*?[\"\']", html, re.IGNORECASE):
            matched_urls.append(url[6:-1])
    return matched_urls



def get_date(article):
    ''' (newspaper.article.Article) -> str
    Searches and returns date of which the article was published
    Returns 'N/A' otherwise

    Keyword arguments:
    article         -- 'Newspaper.Article' object of article
    '''
    dates = []
    for key, value in article.meta_data.iteritems():
        if re.search("date", key, re.IGNORECASE):
            try:
                dt = parser.parse(str(value)).date().strftime("%Y-%m-%d")
                dates.append(dt)
            except:
                pass
    if dates:
        return min(dates)
    return 'N/A'

def get_keywords(article, keywords):
    ''' (newspaper.article.Article, list of str) -> list of str
    Searches and returns keywords which the article contained
    Returns empty list otherwise

    Keyword arguments:
    article         -- 'Newspaper.Article' object of article
    keywords        -- List of keywords
    '''
    matched_keywords = []
    for key in keywords:
        if re.search(key, article.title + article.text, re.IGNORECASE):
            matched_keywords.append(key)
    return matched_keywords

if __name__ == '__main__':
    # a = [['cnn', 'http://cnn.com'], ['nyt', 'http://nytimes.com'],['Yahoo news','http://news.yahoo.com'], ['Google News','http://news.google.com']]
    # a = [a[0]]
    # b = populate_sites(a, True)
    #
    # db.connect('keywords')
    # keywords = db.get_all_keywords()
    # db.close_connection()
    # keywords = ['ebola', 'doctor', 'killed']
    #
    # db.connect('sites')
    # #laterz
    # db.close_connection()
    # sites = ["nytimes.com", 'go.com', 'yahoo.com']
    #
    # db.connect('articles')
    #
    # download_articles(b, keywords, sites, 'articles')



    # from newspaper import Article
    # urls = ["http://www.cnn.com/2014/10/12/living/columbus-day-indigenous-people-day/index.html?hpt=hp_t2",
    #         "http://www.cnn.com/2014/10/12/health/ebola/index.html?hpt=hp_t1",
    #         "http://www.cnn.com/2014/10/10/health/sperm-donor-qa/index.html?hpt=hp_c2",
    #         "http://www.nytimes.com/2014/10/13/world/asia/once-a-symbol-of-power-farming-now-an-economic-drag-in-china.html?hp&action=click&pgtype=Homepage&version=LargeMediaHeadlineSum&module=photo-spot-region&region=top-news&WT.nav=top-news&_r=0",
    #         "http://www.cbc.ca/news/canada/calgary/downtown-calgary-electrical-fire-damage-will-take-days-to-rebuild-1.2796497"]
    # for url in urls:
    #     start = timeit.default_timer()
    #     first_article = Article(url, keep_article_html=True)
    #     first_article.download()
    #     first_article.parse()
    #
    #     print first_article.source_url    # can be used for site i.e. cnn.com
    #     print first_article.authors       # author    Done
    #     print first_article.title         # title     Done
    #     print get_date(first_article)     # date      IP
    #     print first_article.url           # url       Done
    #     print ": " + first_article.article_html + " :"
    #     print first_article.text          # keyword   IP
    #
    #     #print len(match_sources(get_sources(first_article), ['oregonlive.com', 'nytimes.com']) )              # sources   Done
    #     print ""
    #
    # pass
    # db.connect('keywords')
    # a = db.get_keywords()
    # print a
    # #db.add_keywords('Ebola')
    # a = db.get_keywords()
    # print a
    # db.close_connection()


