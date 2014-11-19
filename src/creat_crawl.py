import os
import subprocess
def creat_url(url):
    add_url=url
    crawl = open("CreatWarc.sh", 'w')
    crawl.write("#!/bin/bash \n")
    crawl.write("BASEDIR=$(dirname $0) \n")
    crawl.write("cd crawler\n")
    crawl.write("python crawler.py -u "+url+"\n")
    crawl.write("cd ..\n")
    crawl.write("cd ..\n")  
    crawl.write("mkdir -p warc\n")
    crawl.write("mv ./src/crawler/out.warc.gz ./warc/\n")
    crawl.write("cd ./warc \n")
    add_url=add_url.replace("/","\\\\")
    crawl.write("mv out.warc.gz "+add_url+".warc.gz\n")
    crawl.close()
    os.chmod('./CreatWarc.sh', 0700)
    subprocess.call(['./CreatWarc.sh'])

#if __name__ == '__main__':
    #creat_url("http://www.naturalnews.com/045495_assassination_drones_autonomous_killing_facial_recognition.html")
