import sys
import os

# Add Django directories in the Python paths for django shell to work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'Frontend')))
import django
import warc_creator
os.environ['DJANGO_SETTINGS_MODULE'] = 'Frontend.settings'
from articles.models import*

# setup django
django.setup()
article_file_name = "article_warc.stream"

article_file = open(article_file_name, "a")
for version in Version.objects.all():
     warc_creator.enqueue_article(Article.objects.get(id = version.article_id).url, version.text_hash)
article_file.close()