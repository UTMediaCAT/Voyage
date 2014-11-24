import os
import subprocess

ARTICLE_WARC_DIR = "warc/article"
TWITTER_WARC_DIR = "warc/twitter"

def create_article_warc(url):
    '''
    (url)-->None
    giving url it will export warc file
    
    create_warc("http://www.facebook.com")
    it should have a warc.gz file under 
    ARTICLE_WARC_DIR/http:\\www.facebook.com.warc.gz
    '''
    rename_url=url.replace("/","\\")
    os.chmod('./CreateArticleWarc.sh', 0700)
    subprocess.call(['./CreateArticleWarc.sh',url,rename_url,ARTICLE_WARC_DIR])
    
def create_twitter_warc(url):
    '''
    (url)-->None
    giving url it will export warc file
    
    create_warc("https://twitter.com/LeagueOfLegends")
    it should have a HTML file under 
    TWITTER_WARC_DIR/LeagueOfLegends.html
    '''
    rename_url=url.replace("/","\\")
    url_split=url.split("/")
    rename_html=url_split[len(url_split)-1]
    os.chmod('./CreateTwitterWarc.sh', 0700)
    subprocess.call(['./CreateTwitterWarc.sh',url,rename_url,rename_html,TWITTER_WARC_DIR])  