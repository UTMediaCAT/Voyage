import pymongo
import db_manager as db
import article_explorer
import twitter_explorer

SITES_DB = "sites"
KEYWORDS_DB = "keywords"
ARTICLES_DB = "articles"


def add_site(url, name, is_monitor, influence):
    """(str, str, bool, int) -> None
    Connect to sites collection and add a new site with url as key
    """
    db.connect(SITES_DB)
    try:
        db.add_document({"_id": url,
                        "name": name,
                        "is_monitor": is_monitor,
                        "influence": influence})
        print url + " added."

    # if url already exists
    except pymongo.errors.DuplicateKeyError:
        print url + " already exists."

    db.close_connection()


def add_monitor_site(url, name, influence):
    """(str, str, int) -> None
    Connect to sites collection and add a new monitor site with url as key
    """
    add_site(url, name, True, influence)


def add_foreign_site(url, name, influence):
    """(str, str, int) -> None
    Connect to sites collection and add a new foreign site with url as key
    """
    add_site(url, name, False, influence)


def get_all_sites():
    """(None) -> list of dict of objects
    Connect to sites collection and returns all the sites stored in the database
    """
    db.connect(SITES_DB)
    sites = db.get_all_documents()
    db.close_connection()
    return sites


def get_monitor_sites():
    """(None) -> list of dict of objects
    Connect to sites collection and returns all the monitor sites stored in the database
    """
    db.connect(SITES_DB)
    sites = db.get_documents("is_monitor", True)
    db.close_connection()
    return sites


def get_foreign_sites():
    """(None) -> list of dict of objects
    Connect to sites collection and returns all the foreign sites stored in the database
    """
    db.connect(SITES_DB)
    sites = db.get_documents("is_monitor", False)
    db.close_connection()
    return sites


def get_sites_by_value(field, value):
    """(str, object) -> list of dict of objects
    Connect to sites collection and returns all the sites stored in the
    database that match the field and value query
    Field       : Value
    "_id"       : str
    "name"      : str
    "is_monitor": bool
    "influence" : int
    """
    db.connect(SITES_DB)
    sites = db.get_documents(field, value)
    db.close_connection()
    return sites


def set_site_by_value(url, field, new_value):
    """(str, str, object) -> None
    Connect to sites collection and changes finds the site with id as url
    then changes the field with the new_value
    Field       : Value
    "_id"       : str
    "name"      : str
    "is_monitor": bool
    "influence" : int
    """
    db.connect(SITES_DB)
    db.set_field_value(url, field, new_value)
    print field + " of " + url + " changed to " + str(new_value)
    db.close_connection()


def del_site(url):
    """(str) -> None
    Connect to sites collection and removes a site specified by url
    """
    db.connect(SITES_DB)
    db.del_document(url)
    db.close_connection()
    print url + " removed."


def del_sites(urls=None):
    """(list of str) -> None
    Connect to sites collection and removes all sites specified by url in the list
    If no parameter passed then all sites are removed from the collection
    """
    db.connect(SITES_DB)
    # if urls is not None
    if urls:
        for url in urls:
            db.del_document(url)
            print url + " removed."
    # else empty sites db
    else:
        db.del_all_documents()
        print "All urls removed."
    db.close_connection()


def add_keyword(keyword):
    """(str) -> None
    Connect to keyword collection and add a new keyword to the list
    """
    # if keyword already exists
    if keyword in get_all_keywords():
        print "keyword " + keyword + " already exists."
    # else add the keyword
    else:
        db.connect(KEYWORDS_DB)
        db.add_keyword(keyword)
        print "keyword " + keyword + " added."
        db.close_connection()


def get_all_keywords():
    """(None) -> list of str
    Connect to keyword collection return a list of keywords
    """
    db.connect(KEYWORDS_DB)
    keywords = db.get_all_keywords()
    db.close_connection()
    return keywords


def del_keyword(keyword):
    """(str) -> None
    Connect to keyword collection and delete keyword from the list
    """
    # if keyword does not exist
    if keyword not in get_all_keywords():
        print "keyword " + keyword + " does not exist."
    # else remove the keyword
    else:
        db.connect(KEYWORDS_DB)
        db.del_keyword(keyword)
        print "keyword " + keyword + " deleted."
        db.close_connection()


def del_all_keywords():
    """(None) -> None
    Connect to keyword collection and empty the list of keywords
    """
    db.connect(KEYWORDS_DB)
    db.del_all_keywords()
    print "All keywords deleted."
    db.close_connection()


def run_article_explorer():
    article_explorer.explore(KEYWORDS_DB, SITES_DB, ARTICLES_DB)


def run_twitter_explorer():
    pass

if __name__ == '__main__':
    # add_monitor_site("https://news.google.com/", "Google News", 10)
    # add_site("http://cnn.com", "CNN", True, 2)
    # add_site("http://nytimes.com", "The New York Times", True, 2)
    # add_site("http://time.com", "TIME", True, 2)
    # add_site("http://aljazeera.com/", "Al Jazeera", False, 2)
    # add_site("http://ynetnews.com", "Ynetnews", False, 2)
    # set_site("http://cnn.com", "influence", 3)
    # del_site("https://news.google.com/")
    # #del_sites()     # Removes all sites in the collection
    #
    # print "\n"
    # for site in get_all_sites():
    #     print site
    #
    # print "\n"
    # for site in get_monitor_sites():
    #     print site
    #
    # print "\n"
    # for site in get_foreign_sites():
    #     print site
    #
    # print "\n"
    # for site in get_sites("influence", 2):
    #     print site
    #
    # add_keyword("Canada")
    #
    # print "\n"
    # for keyword in get_all_keywords():
    #     print keyword
    #
    # print "\n"
    # del_site("http://cnn.com")
    # del_site("http://nytimes.com")
    #
    # add_site("http://cnn.com", "CNN", False, 2)
    # add_site("http://nytimes.com", "The New York Times", False, 2)
    #
    # run_article_explorer()

    pass