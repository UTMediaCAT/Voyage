
"""
This script retrieves monitoring site, foreign sites,
and keywords from Mongo database and looks into the monitoring
sites to find matching foreign sites or keywords.
newspaper package is mainly used to extract useful data.
If any keyword (of text) or foreign sites (of links) matched,
all the relevant data will be stored at another Mongo database for Articles
"""

__author__ = "ACME: CSCC01F14 Team 4"
__authors__ = "Yuya Iwabuchi, Jai Sughand, Xiang Wang, Kyle Bridgemohansingh, Ryan Pan"


# newspaper, for populating articles of each site
# and parsing most of the data.
import newspaper
# Used for newspaper's keep_article_html as it was causing error without it
import lxml.html.clean

# Regex, for parsing keywords and sources
import re

# For counting seconds
import time
# For getting today's date
import datetime
# For extracting 'pub_date's
from dateutil import parser

# For connecting with the Database
import db_manager as db

# Settings that will be kept in database later on
STORE_ALL_SOURCES = False       # False             - Stores all links within articles which matched with the keywords
FROM_START = True               # True              - True: Populate all articles from start
DATE_FORMAT = "%Y-%m-%dT%H:%M"  # "%Y-%m-%dT%H:%M"  - Universal date format for consistency
SITE_DB_ID = '_id'
SITE_DB_NAME = 'name'
ARTICLE_DB_ID = '_id'
ARTICLE_DB_DATE = 'date'
ARTICLE_DB_TITLE = 'title'
ARTICLE_DB_PUBDATE = 'pub_date'
ARTICLE_DB_AUTHORS = 'author'
ARTICLE_DB_KEYWORDS = 'keywords'
ARTICLE_DB_SOURCES = 'sources'


def explore(keyword_db, site_db, article_db):
    """ (str, str, str) -> None
    Connects to keyword and site database, crawls within monitoring sites,
    then pushes articles which matches the keywords or foreign sites to the article database

    Keyword arguments:
    keyword_db          -- Keywords database name
    site_db             -- Sites database name
    article_db          -- Article database name
    """

    print "+----------------------------------------------------------+"
    print "| Retrieving data from Database ...                        |"
    print "+----------------------------------------------------------+"

    # Connects to Site Database
    db.connect(site_db)

    monitoring_sites = []
    # Retrieve, store, and print monitoring site information
    print "\nMonitoring Sites\n\t%-25s%-40s" % ("Name", "URL")
    for site in db.get_documents("is_monitor", True):
        # monitoring_sites is now in form [['Name', 'URL'], ...]
        monitoring_sites.append([site[SITE_DB_NAME], site[SITE_DB_ID]])
        print("\t%-25s%-40s" % (site[SITE_DB_NAME], site[SITE_DB_ID]))

    foreign_sites = []
    # Retrieve, store, and print foreign site information
    print "\nForeign Sites\n\t%-25s%-40s" % ("Name", "URL")
    for site in db.get_documents("is_monitor", False):
        # foreign_sites is now in form ['URL', ...]
        foreign_sites.append(site[SITE_DB_ID])
        print("\t%-25s%-40s" % (site['name'], site[SITE_DB_ID]))
        
    # Close connection with Site Database
    db.close_connection()

    # Connects to Keyword Database
    db.connect(keyword_db)
    # Retrieve all stored keywords
    keywords = db.get_all_elements()
    # Close connection with Keyord Database
    # Print all the keywords
    db.close_connection()
    print "\nKeywords:"
    for key in keywords:
        print "\t%s" % key

    print "\n"

    print "+----------------------------------------------------------+"
    print "| Populating sites ...                                     |"
    print "+----------------------------------------------------------+"
    # Populate the monitoring sites with articles
    populated_sites = populate_sites(monitoring_sites)

    print "\n"

    print "+----------------------------------------------------------+"
    print "| Evaluating Articles ...                                  |"
    print "+----------------------------------------------------------+"
    # Parse the articles in all sites
    parse_articles(populated_sites, keywords, foreign_sites, article_db)


def populate_sites(sites):
    """ (list of str) -> list of [str, newspaper.source.Source]
    Searches through the sites using newspaper library and
    returns list of sites with available articles populated

    Keyword arguments:
    sites         -- List of [name, url] of each site
    """
    new_sites = []
    
    # Populate each Sites, then print the amount of articles and time it took
    print "\n\t%-25s%10s%10s" % ("Site", "Articles", "Time")
    for s in range(len(sites)):
        print("\t%-24s" % (sites[s][0])),
        # To count the time
        start = time.time()
        # Duplicate the name of the sites
        new_sites.append([sites[s][0]])

        # Use the url and populate the site with articles
        new_sites[s].append((newspaper.build(sites[s][1],
                                             memoize_articles=not FROM_START,
                                             keep_article_html=True,
                                             fetch_images=False,
                                             language='en')))
        end = time.time()
        # report back the amount of articles found, and time it took
        print("%6i pgs%9is" % (new_sites[s][1].size(), end - start))
    # return the list
    return new_sites


def parse_articles(populated_sites, db_keywords, foreign_sites, db_name):
    """ (list of [str, newspaper.source.Source], list of str, list of str, str) -> None
    Download all articles from built sites and stores information to the database

    Keyword arguments:
    populated_sites     -- List of [name, 'built_article'] of each site
    total_threads       -- Number of threads to use for downloading per sites.
                           This can greatly increase the speed of download
    """
    added, updated, failed, no_match = 0, 0, 0, 0
    start = time.time()
    
    # connect to Article Database
    db.connect(db_name)

    # Collect today's date and time
    today = datetime.datetime.now().strftime(DATE_FORMAT)

    print("\nStore All Sources: %s" % str(STORE_ALL_SOURCES))
    # for each article in each sites, download and parse important data
    for site in populated_sites:
        print "\n%s" % site[0]
        for art in site[1].articles:
            url = art.url
            print "\n\tURL:      ", url
            print "\tEvaluating ...\r",
            # Try to download and extract the useful data
            try:
                art.download()
                art.parse()
                title = art.title
            except:
                title = ""
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
                if not (keywords == [] and (sources == [] or STORE_ALL_SOURCES)):
                    # Try to add all the data to the Article Database
                    try:
                        db.add_document({ARTICLE_DB_ID: url, ARTICLE_DB_DATE: today, ARTICLE_DB_TITLE: title,
                                         ARTICLE_DB_PUBDATE: pub_date, ARTICLE_DB_AUTHORS: authors,
                                         ARTICLE_DB_KEYWORDS: keywords, ARTICLE_DB_SOURCES: sources})
                        added += 1
                        print "\tResult:    Match detected! Added to the database."
                    # Most common errors are document already existing, thus delete then resubmit
                    except:
                        db.del_document(url)
                        db.add_document({ARTICLE_DB_ID: url, ARTICLE_DB_DATE: today, ARTICLE_DB_TITLE: title,
                                         ARTICLE_DB_PUBDATE: pub_date, ARTICLE_DB_AUTHORS: authors,
                                         ARTICLE_DB_KEYWORDS: keywords, ARTICLE_DB_SOURCES: sources})
                        print "\tResult:    Match detected! Article already in database. Updating."
                        updated += 1
                else:
                    no_match += 1
                    print "\tResult:    No Match Detected."
            else:
                print "\tResult:    Failed to download!"
                failed += 1
            # Some stats to look at while running the script
            print("\n\tStatistics\n\tAdded: %i | Updated: %i | No Match: %i | Failed: %i | Time Elapsed: %is" %
                  (added, updated, no_match, failed, time.time() - start))
            print "+--------------------------------------------------------------------+"
    print("Finished parsing all sites!")
    db.close_connection()


def get_sources(html, sites):
    """ (str, list of str) -> list of str
    Searches and returns links redirected to sites within the html
    Returns empty list if none found

    Keyword arguments:
    html                -- string of html
    sites               -- list of site urls to look for
    """
    matched_urls = []

    # for each site, check if it exists within the html given
    for site in sites:
        if STORE_ALL_SOURCES:
            for url in re.findall("href=[\"\'][^\"\']*?.*?[^\"\']*?[\"\']", html, re.IGNORECASE):
                # If it matches even once, append the site to the list
                matched_urls.append(url[6:-1])
        else:
            for url in re.findall("href=[\"\'][^\"\']*?" + re.escape(site) + "[^\"\']*?[\"\']", html, re.IGNORECASE):
                # If it matches even once, append the site to the list
                matched_urls.append(url[6:-1])
    # Return the list
    return matched_urls


def get_pub_date(article):
    """ (newspaper.article.Article) -> str
    Searches and returns date of which the article was published
    Returns 'N/A' otherwise

    Keyword arguments:
    article         -- 'Newspaper.Article' object of article
    """
    dates = []

    # For each metadata stored by newspaper's parsing ability, check if any of the key contains 'date'
    for key, value in article.meta_data.iteritems():
        if re.search("date", key, re.IGNORECASE):
            # If the key contains 'date', try to parse the value as date
            try:
                dt = parser.parse(str(value)).date().strftime(DATE_FORMAT)
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
    """ (newspaper.article.Article, list of str) -> list of str
    Searches and returns keywords which the article's title or text contains
    Returns empty list otherwise

    Keyword arguments:
    article         -- 'Newspaper.Article' object of article
    keywords        -- List of keywords
    """
    matched_keywords = []

    # For each keyword, check if article's text contains it
    for key in keywords:
        if re.search(key, article.title + article.text, re.IGNORECASE):
            # If the article's text contains the key, append it to the list
            matched_keywords.append(key)
    # Return the list
    return matched_keywords


if __name__ == '__main__':

    # explore('keywords', 'sites', 'articles')
    pass