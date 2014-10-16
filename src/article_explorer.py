
"""
This script retrieves monitoring site, foreign sites,
and keywords from Mongo database and looks into the monitoring
sites to find matching foreign sites or keywords.
If found, all the data will be stored at another
Mongo database specialized for Articles
"""


# newspaper -- For more information, go to
import newspaper
from newspaper import news_pool
from newspaper import Article
import lxml.html.clean

#regex
import re

#Times
import time
import datetime
#dateutil
from dateutil import parser

#db_manager
import db_manager as db

def run(keyword_db, site_db, article_db):
    ''' (str, str, str) -> None
    Connects to keyword and site database, crawls within monitoring sites,
    then pushes articles which matches the keywords or foreign sites to the article database

    Keyword arguments:
    keyword_db      -- Keywords database name
    site_db         -- Sites database name
    article_db      -- Article database name
    '''


    print "+----------------------------------------------------------+"
    print "| Retrieving data from Database ...                        |"
    print "+----------------------------------------------------------+"

    # Connects to Site Database
    db.connect(site_db)

    monitoring_sites = []
    # Retrieve, store, and print monitoring site information
    print "\nMonitoring Sites\n\t%-25s%-40s"%("Name", "URL")
    for site in db.get_document("is_monitor", True):
        # monitoring_sites is now in form [['Name', 'URL'], ...]
        monitoring_sites.append([site['name'], site['_id']])
        print("\t%-25s%-40s"%(site['name'], site['_id']))

    foreign_sites = []
    # Retrieve, store, and print foreign site information
    print "\nForeign Sites\n\t%-25s%-40s"%("Name", "URL")
    for site in db.get_document("is_monitor", False):
        # foreign_sites is now in form ['URL', ...]
        foreign_sites.append(site['_id'])
        print("\t%-25s%-40s"%(site['name'], site['_id']))
        
    # Close connection with Site Database
    db.close_connection()

    # Connects to Keyword Database
    db.connect(keyword_db)
    # Retrieve all stored keywords
    keywords = db.get_all_keywords()
    # Close connection with Keyord Database
    # Print all the keywords
    db.close_connection()
    print "\nKeywords:"
    for key in keywords:
        print "\t%s"%key

    print "\n"

    print "+----------------------------------------------------------+"
    print "| Populating sites ...                                     |"
    print "+----------------------------------------------------------+"
    # Populate the monitoring sites with articles
    populated_sites = populate_sites(monitoring_sites, True)

    print "\n"

    print "+----------------------------------------------------------+"
    print "| Evaluating Articles ...                                  |"
    print "+----------------------------------------------------------+"
    # Parse the articles in all sites
    parse_articles(populated_sites, keywords, foreign_sites, article_db)



def populate_sites(sites, from_start):
    ''' (list of str, bool) -> list of [str, newspaper.source.Source]
    Searches through the sites using newspaper library and
    returns list of sites with available articles populated

    Keyword arguments:
    sites         -- List of [name, url] of each site
    from_start    -- Boolean to search sites from scratch
    '''
    new_sites = []
    
    # Populate each Sites, then print the amount of articles and time it took
    print "\n\t%-25s%10s%10s"%("Site", "Articles", "Time")
    for s in range(len(sites)):
        print ("\t%-24s"%(sites[s][0])),
        # To count the time
        start = time.time()
        # Duplicate the name of the sites
        new_sites.append([sites[s][0]])

        # Use the url and populate the site with articles
        new_sites[s].append((newspaper.build(sites[s][1],
                                             memoize_articles=not from_start,
                                             keep_article_html=True,
                                             fetch_images=False,
                                             language='en')))
        end = time.time()
        # report back the amount of articles found, and time it took
        print ("%6i pgs%9is"%(new_sites[s][1].size(), end - start))
    # return the list
    return new_sites

def parse_articles(populated_sites, db_keywords, foreign_sites, db_name):
    ''' (list of [str, newspaper.source.Source], list of str, list of str, str) -> None
    Download all articles from built sites and stores the metadata
    to the database

    Keyword arguments:
    populated_sites -- List of [name, 'built_article'] of each site
    total_threads   -- Number of threads to use for downloading per sites.
                       This can greatly increase the speed of download
    '''
    added, failed,no_match = 0,0,0
    start = time.time()
    
    # connect to Article Database
    db.connect(db_name)

    # Collect today's date and time
    today = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    
    # for each article in each sites, download and parse important data
    for site in populated_sites:
        print "\n%s"%site[0]
        for art in site[1].articles:
            url =  art.url
            print "\n\tURL:      ", url
            print "\tEvaluating ...\r",
            # Try to download and extract the useful data
            try:
                art.download()
                art.parse()
                title = art.title
            except:
                title == ""
            # If downloading/parsing the page fails, stop here and move on to next article
            if not ((title == "") or (title == "Page not found")):
                # Regex the keyword from the article's text
                keywords = get_keywords(art, db_keywords)
                # Regex the links within article's html
                sources = get_sources(art.article_html, foreign_sites)
                # Store parsed author
                authors = art.authors
                # Try to parse the published date
                pub_date = get_pub_date(art)

                # Print all data accordingly
                print "\tTitle:    ", title
                print "\tAuthor:   ", authors
                print "\tDate:     ", pub_date
                print "\tKeywords: ", keywords
                print "\tSources:  ", sources

                # If neither of keyword nor sources matched, then stop here and move on to next article
                if not (keywords == [] and sources == []):
                    # Try to add all the data to the Article Database
                    try:
                        db.add_document({"_id": url, "date": today, "title": title,
                                         "pub_date": pub_date, "author": authors,
                                         "keywords": keywords, "sources": sources})
                        added += 1
                        print "\tResult:    Match detected! Added to the database."
                    # Most common errors are document already existing, thus print accordingly
                    except:
                        print "\tResult:    Match detected! Article already in the database."


                else:
                    no_match += 1
                    print "\tResult:    No Match Detected."
            else:
                print "\tResult:    Failed to download!"
                failed += 1
            # Some stats to look at while running the script
            print ("\nStatistics\n\tAdded: %i pgs  Failed: %i pgs  No Match: %i pgs  Time Elapsed: %is"%
                   (added,failed,no_match, time.time() - start))
            print "+--------------------------------------------------------------------+"


def get_sources(html, sites):
    ''' (str, list of str) -> list of str
    Searches and returns links redirected to sites within the html
    Returns empty list if none found

    Keyword arguments:
    html            -- string of html
    sites           -- List of site urls to look for
    '''
    matched_urls = []

    # for each site, check if it exists within the html given
    for site in sites:
        for url in re.findall("href=[\"\'][^\"\']*?" + re.escape(site) + "[^\"\']*?[\"\']", html, re.IGNORECASE):
            # If it matches even once, append the site to the list
            matched_urls.append(url[6:-1])
    # Return the list
    return matched_urls



def get_pub_date(article):
    ''' (newspaper.article.Article) -> str
    Searches and returns date of which the article was published
    Returns 'N/A' otherwise

    Keyword arguments:
    article         -- 'Newspaper.Article' object of article
    '''
    dates = []

    # For each metadata stored by newspaper's parsing ability, check if any of the key contains 'date'
    for key, value in article.meta_data.iteritems():
        if re.search("date", key, re.IGNORECASE):
            # If the key contains 'date', try to parse the value as date
            try:
                dt = parser.parse(str(value)).date().strftime("%Y-%m-%dT%H:%M")
                # If parsing succeeded, then append it to the list
                dates.append(dt)
            except:
                pass
    # If one of more dates were found,
    # return the oldest date as new ones can be updated dates instead of published dates
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

    # For each keyword, check if article's text contains it
    for key in keywords:
        if re.search(key, article.title + article.text, re.IGNORECASE):
            # If the article's text contains the key, append it to the list
            matched_keywords.append(key)
    # Return the list
    return matched_keywords


if __name__ == '__main__':

    # run('keywords', 'sites', 'articles')

    pass