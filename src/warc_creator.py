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

def create_article_warc(url):
    '''
    (url)-->None
    giving url it will export warc file
    
    create_warc("http://www.facebook.com")
    it should have a warc.gz file under 
    ARTICLE_WARC_DIR/http:\\www.facebook.com.warc.gz
    '''
    config = configuration()['warc']
    rename_url = url.replace("/", "_")
    os.chmod('./CreateArticleWarc.sh', 0700)
    command = './CreateArticleWarc.sh %s %s %s' % (url, rename_url, config['dir'] + "/" + config['article_subdir'])
    subprocess.call(command, shell = True)
    
def create_twitter_warc(url):
    '''
    (url)-->None
    giving url it will export warc file
    
    create_warc("https://twitter.com/LeagueOfLegends")
    it should have a HTML file under 
    TWITTER_WARC_DIR/https:\\twitter.com\LeagueOfLegends
    '''
    config = configuration()['warc']
    
    rename_url = url.replace("/", "_")
    os.chmod('./CreateTwitterWarc.sh', 0700)
    command = "./CreateTwitterWarc.sh %s %s %s" % (url, rename_url, config['dir'] + "/" + config['twitter_subdir'])
    # command = ["./CreateTwitterWarc.sh", url, rename_url, config['dir'] + "/" + config['twitter_subdir']]
    # os.execlp("./CreateTwitterWarc.sh", url, rename_url, config['dir'] + "/" + config['twitter_subdir')
    subprocess.Popen(command, shell = True)    