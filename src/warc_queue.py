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
	max_phantoms = 2
	wait_time = 5

	article_queue = []
	article_processes = []
	while (True):
		while (len(article_processes) >= max_phantoms):
			article_processes[:] = [p for p in article_processes if p.poll() is None]
			time.sleep(wait_time)

		article_file_name = "article_warc.stream"
		#if not tasks remaining, retry thoes url that fialed before
		if os.stat(article_file_name).st_size == 0:
			article_file_name = "article_warc.stream.failure"

		article_file = open(article_file_name, "r+")
		for url in article_file:
			if (url.strip() != ""):
				article_queue.append(url.strip())
		article_file.seek(0)
		article_file.truncate()
		article_file.close()

		if (len(article_queue) > 0):
			url = article_queue.pop(0)
			article_processes.append(warc_creator.create_article_warc(url))

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
				if num_polls > 600:
					p.terminate()
					fail_name = "article_warc.stream.failure"
					fail = open(fail_name, "a")
					fail.write(url + "\n")
					fail.close()
					break

			article_processes.append(p)

		article_processes[:] = [p for p in article_processes if p.poll() is None]

		time.sleep(wait_time)