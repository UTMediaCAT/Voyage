import subprocess
import yaml
import logging

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
    logging.info("creating warc \"{0}\" in \"{1}\"".format(rename_url, dir))
    subprocess.call(["mkdir", "-p", dir], cwd="..", close_fds=True)
    subprocess.Popen(["wpull", "--user-agent 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36' --no-robots --no-check-certificate --no-cookies --timeout 5 --session-timeout 5  --phantomjs --phantomjs-max-time 120", "--warc-file " + rename_url, "-O", "/dev/null", url], cwd="../"+dir, close_fds=True)

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
