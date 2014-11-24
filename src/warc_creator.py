import os
import subprocess

def create_warc(url):
    rename_url=url.replace("/","\\")
    os.chmod('./CreateWarc.sh', 0700)
    subprocess.call(['./CreateWarc.sh',url,rename_url])     