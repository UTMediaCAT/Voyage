import os
import subprocess

def create_warc(url,folderName):
    '''
    (url,Folder_Name)-->None
    giving url and type(article/twitter) it will export warc file
    
    create_warc("http://www.facebook.com","article")
    it should have a warc.gz file under 
    ./warc/article/http:\\www.facebook.com.warc.gz
    '''
    rename_url=url.replace("/","\\")
    os.chmod('./CreateWarc.sh', 0700)
    subprocess.call(['./CreateWarc.sh',url,rename_url,folderName])

create_warc("http://nation.time.com/2013/01/08/an-army-ranger-turned-refugee-helper/","jai")