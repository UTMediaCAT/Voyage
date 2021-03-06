import subprocess
#import yaml
import logging
#import common
import time



def create_warc(url, file_name, directory):
    """
    creates a warc file from url and places it in dest
    """
    logging.info("creating warc \"{0}\" as \"{1}\" in \"{2}\"".format(url, file_name, directory))
    subprocess.call(["mkdir", "-p", directory], cwd="..", close_fds=True)   # "--reject-regex", ".*(api\.[A-Za-z0-9]*\.com).*, ",
    print("THE URL IS :  {0} \n".format(url))
    time.sleep(2)
    return subprocess.Popen(["wpull", "--user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36", "--no-robots", "--no-check-certificate", "--no-cookies", "--waitretry", "2" ,"--random-wait", "--phantomjs", "--no-phantomjs-snapshot", "--phantomjs-max-time", "150", "--no-warc-keep-log", "--quiet","--delete-after","--warc-file", file_name,  url], cwd="../"+directory, close_fds=True)

def create_pdf(url, file_name, directory):
    """
    creates a pdf file from url and places it in dest
    """
    logging.info("creating pdf \"{0}\" as \"{1}\" in \"{2}\"".format(url, file_name, directory))
    subprocess.call(["mkdir", "-p", directory], cwd="..", close_fds=True)
#https://forward.com/fast-forward/416924/breitbart-news-columnist-caroline-glick-joins-new-right-wing-party-in/
    # create png and img file
    return subprocess.Popen(["phantomjs", "../../src/rasterize.js", url,  file_name], cwd="../"+directory, close_fds=True)

def enqueue_article(url, file_name, directory = "."):
    """(url)-->None
    Saves the url into article queue file for warc_queue.py to pick up and download
    """
    article_file_name = directory + "/" + "article_warc.stream"
    article_file = open(article_file_name, "a")
    article_file.write((url + " " + file_name + "\n"))
    article_file.close()


def create_article_warc(url, file_name):
    """(url)-->None
    giving url it will export warc file

    create_warc("http://www.facebook.com")
    it should have a warc.gz file under
    ARTICLE_WARC_DIR/http:__www.facebook.com.warc.gz
    """

    #config = common.get_config()["warc"]
    return create_warc(url, file_name, "warc" + "/" + "article")


def create_twitter_warc(url):
    """(url)-->None
    giving url it will export warc file

    create_warc("https://twitter.com/LeagueOfLegends")
    it should have a HTML file under
    TWITTER_WARC_DIR/https:__twitter.com_LeagueOfLegends
    """
    file_name = url.replace("/", "_")
    #config = common.get_config()["warc"]
    return create_warc(url, file_name, "warc" + "/" + "twitter")


def create_article_pdf(url, file_name):
    """(url)-->None
    giving url it will export pdf file

    create_article_pdf("http://www.facebook.com")
    it should have a .pdf file under
    ARTICLE_WARC_DIR/http:__www.facebook.com.pdf
    """
    #config = common.get_config()["pdf"]
    return create_pdf(url, file_name, "warc" + "/" + "article")
