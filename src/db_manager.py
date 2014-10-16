from pymongo import *


# Database Information
DB_USER_ID = "acme"
DB_USER_PSW = "cscc01"
DB_URL = "mongodb://" + DB_USER_ID + ":" + DB_USER_PSW + "@ds039960.mongolab.com:39960/cscc01-acme"
DB_NAME = "cscc01-acme"


# connection functions
def connect(collection_name):
    """(str) -> None
    Connect to database and get a collection by collection_name
    """
    global client
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    global COLLECTION
    COLLECTION = db[collection_name]


def close_connection():
    """(None) -> None
    Close the connection to database
    """
    client.close()

# universal functions fot sites, articles sites and tweets


def add_document(new_document):
    """(dict) -> None
    Add new_document to COLLECTION
    """
    COLLECTION.insert(new_document)


def get_documents(field, value):
    """(str, object) -> list of dict
    Return a document from COLLECTION by given url
    """
    list_doc = []
    documents = COLLECTION.find({field: value})
    for element in documents:
        list_doc.append(element)
    return list_doc


def get_all_documents():
    """(None) -> a list of dict
    Return a list of documents from COLLECTION
    """    
    list_doc = []
    documents = COLLECTION.find()
    for element in documents:
        list_doc.append(element)
    return list_doc


def set_field_value(url, field, value):
    """(str, str, anyType) -> None
    Set the the value of field of the document given by url
    """
    COLLECTION.update({'_id': url}, {'$set': {field: value}})


def del_document(url):
    """(str) -> None
    Delete the document given by url from the COLLECTION
    """
    COLLECTION.remove({'_id': url})


def del_all_documents():
    """(str) -> None
    Delete the document given by url from the COLLECTION
    """
    COLLECTION.remove({})

#Keyword functions


def add_keyword(key_word):
    """(str) -> None
    Add a new key_word to the list in COLLECTION
    """
    COLLECTION.update({'_id': 1}, {'$push': {"list": key_word}})


def get_all_keywords():
    """(None) - > list of str
    Return a list of keywords in COLLECTION
    """
    keywords = COLLECTION.find_one()["list"]
    return keywords


def del_keyword(key_word):
    """(str) - > None
    Delete key_word from the list in COLLECTION
    """    
    COLLECTION.update({'_id': 1}, {'$pull': {"list": key_word}})


def del_all_keywords():
    """(None) - > None
    Empty the list of keywords in COLLECTION
    """       
    keywords = COLLECTION.find_one()["list"]
    for keyword in keywords:
        COLLECTION.update({'_id': 1}, {'$pull': {"list": keyword}})