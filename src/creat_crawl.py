import os
import subprocess
class creat_crawl():
    def __init__(self):
        pass
    
    def creat_url(self,url):
        add_url=url
        crawl = open("Crawl.sh", 'w')
        crawl.write("#!/bin/bash \n")
        crawl.write("BASEDIR=$(dirname $0) \n")
        crawl.write("cd $BASEDIR \n")
        crawl.write("python crawler.py -u "+url+"\n")
        crawl.write("cd ..\n")
        crawl.write("mkdir -p warc\n")
        crawl.write("mv ./src/out.warc.gz ./warc/\n")
        crawl.write("cd ./warc \n")
        add_url=add_url.replace("http://","")
        crawl.write("mv out.warc.gz "+add_url+".warc.gz\n")
        crawl.close()
        os.chmod('./Crawl.sh', 0700)
        subprocess.call(['./Crawl.sh'])

#if __name__ == '__main__':
    #gs=creat_crawl()
    #gs.creat_url("http://www.facebook.ca")
