__author__ = 'sughandj'

import sys
import os
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'Frontend')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'
django.setup()

import commands
import warc_creator

max_phantoms = 4
wait_time = 2
article_file_name = "article_warc_comm.stream"

article_queue = []
while (True):
	while (commands.getoutput('ps').count('phantomjs') >= max_phantoms):
		wait(wait_time)

	article_file = open(article_file_name, "r+")
	for url in article_file:
		article_queue.append(url.strip())
	article_file.seek(0)
	article_file.truncate()
	article_file.close()

	url = article_queue.pop(0)
	warc_creator.create_article_warc(url)
	warc_creator.create_article_pdf(url)