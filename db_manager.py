from pymongo import *

''' INPUTS '''

# Database Information
DB_USER_ID = "acme"
DB_USER_PSW = "cscc01"
DB_URL = "mongodb://" + DB_USER_ID + ":" + DB_USER_PSW + "@ds039960.mongolab.com:39960/cscc01-acme"
DB_NAME = "cscc01-acme"

# HELPER functions (connect)
def connect(collection_name):
    '''Connect to database'''
    global client
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    global COLLECTION
    COLLECTION = db[collection_name]
    print(COLLECTION.find_one())

def close_connection():
    client.close()

#Site functions

def add_site(Monitor, Name, URL, Influence):
    


def get_site(Name):
    pass
    #return site


def set_site(Name, Field, Value):
    pass
    #return none


def del_site(Name):
    pass
    #return None


#Keyword functions

def add_keyword(Keyword):
    pass
    #return none


def del_keyword(Keyword):
    pass
    #return None


def get_keywords():
    pass
    #return list of keywords


''' OUTPUTS '''

#Article functions

def add_article(url, title, date, author, keywords, sources):
    pass
    #return None


def get_article(field, value):
    pass
    #return list of articles


def del_article(url):
    pass
    #return none

