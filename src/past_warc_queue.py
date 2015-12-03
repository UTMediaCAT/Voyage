import sys
import os

# Add Django directories in the Python paths for django shell to work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'Frontend')))

import commands
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'
from articles.models import*

article_file_name = "article_warc.stream"

article_file = open(article_file_name, "a")
for article in Article.objects.all():
	article_file.write(article.url.encode("utf-8") + "\n")
article_file.close()