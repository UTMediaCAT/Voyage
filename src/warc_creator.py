import os
import subprocess
import yaml


def configuration():
    """ (None) -> dict
    Returns a dictionary containing the micro settings from the
    config.yaml file located in the directory containing this file
    """
    config_yaml = open("../config.yaml", 'r')
    config = yaml.load(config_yaml)
    config_yaml.close()
    return config

def create_warc(url, dir):
    """
    creates a warc file from url and places it in dest
    """
    rename_url = url.replace("/", "_")
    subprocess.call(["mkdir", "-p", dir])
    subprocess.Popen(["wget", "--warc-file=" + rename_url, "-O", "/dev/null", url])

def create_article_warc(url):
    """(url)-->None
    giving url it will export warc file

    create_warc("http://www.facebook.com")
    it should have a warc.gz file under
    ARTICLE_WARC_DIR/http:__www.facebook.com.warc.gz
    """
    config = configuration()['warc']
    create_warc(url, config['dir'] + "/" + config['article_subdir'])


def create_twitter_warc(url):
    """(url)-->None
    giving url it will export warc file

    create_warc("https://twitter.com/LeagueOfLegends")
    it should have a HTML file under
    TWITTER_WARC_DIR/https:__twitter.com_LeagueOfLegends
    """
    config = configuration()['warc']
    create_warc(url, config['dir'] + "/" + config['twitter_subdir'])
