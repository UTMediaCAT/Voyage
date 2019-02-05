'''
This script runs as  a task queue for warc, pdf and img generator. It limits the maximum number of process that
generates warc, pdf and img so that the host will not get overloaded.
This script will automatically run along with the server. It will terminates when server stopped running.
'''
__authors__ = 'sughandj', 'wangx173'

import sys
import os
# import django

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
#                                              'Frontend')))
# os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'

import time
import common
import warc_creator

if __name__ == "__main__":

    # number of phantomjs process can be run at a time
    max_phantoms = 4#common.get_config()["warc"]["max_phantoms"]
    # amount of time between 2 iterations (secs)
    wait_time = 5
    article_queue = []
    article_processes = []

    # The process keeps running in the background
    while (True):
        while (len(article_processes) >= max_phantoms):
            time.sleep(0.5)
            article_processes[:] = [p for p in article_processes if p.poll() is None]
            time.sleep(wait_time)
        # article_warc.stream is the temporary file storing the list of urls(or tasks) that need to run.
        article_file_name = "article_warc.stream"
        # if not tasks remaining, retry thoes url that failed before
        time.sleep(0.5)

        if os.stat(article_file_name).st_size == 0:
            article_file_name = "article_warc.stream.failure"
        # read the file and get all the urls
        article_file = open(article_file_name, "r+")
        for line in article_file:

            if (len(line.split(' ')) == 2 and not line.split(' ') in article_queue):
                article_queue.append(line.split(' '))

        article_file.seek(0)
        article_file.truncate()
        article_file.close()

        if (len(article_queue) > 0):

            # get first element in the queue
            line = article_queue.pop(0)
            url = line[0]
            warc_file_name = line[1].strip()
            print('processing: ' + url + ' : ' + warc_file_name)
            article_processes.append(warc_creator.create_article_warc(url, warc_file_name))

            # set time out for pdf generator
            p = warc_creator.create_article_pdf(url, warc_file_name)
            # wait for 200 seconds, if timeout, kill the process
            num_polls = 0

            while p.poll() is None:

                # Waiting for the process to finish.
                time.sleep(0.1)  # Avoid being a CPU busy loop.
                num_polls += 1
                if num_polls > 2000:  # after 150 secs, it will be considered as failure,
					# the process will be terminated and put into failure list
                    time.sleep(0.5)

                    p.terminate()
                    fail_name = "article_warc.stream.failure"
                    fail = open(fail_name, "a")
                    fail.write(url + "\n")
                    fail.close()
                    break

            article_processes.append(p)
        temp = []
        # article_processes[:] = [p for p in article_processes if p.poll() is None]
        for p in article_processes:
            if p.poll() is None:
                temp.append(p)
        article_processes = temp

		# wait wait_time before next iteration
        time.sleep(wait_time)
