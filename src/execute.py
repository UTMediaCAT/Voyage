from article_explorer import *
from twitter_explorer import *
import pymongo

def add_site(url, name, is_monitor, influence):
    '''(str, str, bool, int) -> None
    Connect to sites collection and add a new site with url as key
    '''
    db.connect('sites')
    try:
        db.add_document({"_id": url,
                        "name": name,
                        "is_monitor": is_monitor,
                        "influence": influence})
        print url + " added."

    except pymongo.errors.DuplicateKeyError:
        print url + " already exists."

    db.close_connection()

def add_monitor_site(url, name, influence):
    '''(str, str, int) -> None
    Connect to sites collection and add a new monitor site with url as key
    '''
    add_site(url, name, True, influence)

def add_foreign_site(url, name, influence):
    '''(str, str, int) -> None
    Connect to sites collection and add a new foreign site with url as key
    '''
    add_site(url, name, False, influence)

def remove_site(url):
    '''(str) -> None
    Connect to sites collection and removes a site specified by url
    '''
    db.connect('sites')
    db.del_document(url)
    db.close_connection()
    print url + " removed."

def remove_sites(urls=None):
    '''(list of str) -> None
    Connect to sites collection and removes all sites specified by url in the list
    If no parameter passed then all sites are removed from the collection
    '''
    db.connect('sites')
    if urls:
        for url in urls:
            db.del_document(url)
            print url + " removed."
    else:
        db.del_all_documents()
        print "All urls removed."
    db.close_connection()

if __name__ == '__main__':
    add_monitor_site("https://news.google.com/", "Google News", 10)
    add_site("http://cnn.com", "CNN", True, 2)
    add_site("http://nytimes.com", "The New York Times", True, 2)
    add_site("http://time.com", "TIME", True, 2)
    add_site("http://aljazeera.com/", "Al Jazeera", False, 2)
    add_site("http://ynetnews.com", "Ynetnews", False, 2)
    remove_site("https://news.google.com/")
    #remove_sites()     # Removes all sites in the collection