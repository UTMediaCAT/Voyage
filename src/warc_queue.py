__author__ = 'sughandj'

import sys
import os
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'Frontend')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'
django.setup()

import time
import signal
import commands
import warc_creator


if __name__ == "__main__":
	max_phantoms = 5
	wait_time = 5
	article_file_name = "article_warc.stream"

	article_queue = []
	article_processes = []
	while (True):
		while (len(article_processes) >= max_phantoms):
			article_processes[:] = [p for p in article_processes if p.poll() is None]
			time.sleep(wait_time)

		article_file = open(article_file_name, "r+")
		for url in article_file:
			if (url.strip() != ""):
				article_queue.append(url.strip())
		article_file.seek(0)
		article_file.truncate()
		article_file.close()

		if (len(article_queue) > 0):
			url = article_queue.pop(0)
			#article_processes.append(warc_creator.create_article_warc(url))

			'''
			set time out for pdf generator
			'''
			p = warc_creator.create_article_pdf(url)

			#wait for 30 seconds, if timeout, kill the process
			num_polls = 0
			while p.poll() is None:
				# Waiting for the process to finish.
				time.sleep(0.1)  # Avoid being a CPU busy loop.
				num_polls += 1
				if num_polls > 400:
					p.kill()
					article_queue.append(url)

			article_processes.append(p)



		article_processes[:] = [p for p in article_processes if p.poll() is None]

		time.sleep(wait_time)