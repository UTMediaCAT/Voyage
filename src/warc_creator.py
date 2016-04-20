import subprocess
import yaml
import logging
import threading
import os

# dir of this file
dir = os.path.dirname(os.path.abspath(__file__))

def configuration():
    """ (None) -> dict
    Returns a dictionary containing the micro settings from the
    config.yaml file located in the directory containing this file
    """
    config_yaml = open(dir + "/../config.yaml", 'r')
    config = yaml.load(config_yaml)
    config_yaml.close()
    return config


def create_warc(url, dir):
    """
    creates a warc file from url and places it in dest
    """
    rename_url = url.replace("/", "_")
    logging.info("creating warc \"{0}\" in \"{1}\"".format(rename_url, dir))
    subprocess.call(["mkdir", "-p", dir], cwd="..", close_fds=True)
    return subprocess.Popen(["wpull", "--user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36", "--no-robots", "--no-check-certificate", "--no-cookies", "--random-wait", "--phantomjs", "--no-phantomjs-snapshot", "--phantomjs-max-time", "150", "--warc-file", rename_url,  url], cwd="../"+dir, close_fds=True)


def create_pdf(url, dir):
    """
    creates a pdf file from url and places it in dest
    """
    rename_url = url.replace("/", "_")
    logging.info("creating pdf \"{0}\" in \"{1}\"".format(rename_url, dir))
    subprocess.call(["mkdir", "-p", dir], cwd="..", close_fds=True)

    # create png and img file
    return subprocess.Popen(["phantomjs", "../../src/rasterize.js", url,  rename_url], cwd="../"+dir, close_fds=True)

def enqueue_article(url):
    """(url)-->None
    Saves the url into article queue file for warc_queue.py to pick up and download
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    article_file_name = dir + "/" + "article_warc.stream"
    article_file = open(article_file_name, "a")
    article_file.write(url + "\n")
    article_file.close()


def create_article_warc(url):
    """(url)-->None
    giving url it will export warc file

    create_warc("http://www.facebook.com")
    it should have a warc.gz file under
    ARTICLE_WARC_DIR/http:__www.facebook.com.warc.gz
    """
    config = configuration()['warc']
    return create_warc(url, config['dir'] + "/" + config['article_subdir'])


def create_twitter_warc(url):
    """(url)-->None
    giving url it will export warc file

    create_warc("https://twitter.com/LeagueOfLegends")
    it should have a HTML file under
    TWITTER_WARC_DIR/https:__twitter.com_LeagueOfLegends
    """
    config = configuration()['warc']
    return create_warc(url, config['dir'] + "/" + config['twitter_subdir'])


def create_article_pdf(url):
    """(url)-->None
    giving url it will export pdf file

    create_article_pdf("http://www.facebook.com")
    it should have a .pdf file under
    ARTICLE_WARC_DIR/http:__www.facebook.com.pdf
    """
    config = configuration()['pdf']
    return create_pdf(url, config['dir'] + "/" + config['article_subdir'])
