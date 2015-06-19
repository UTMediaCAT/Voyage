import newspaper
from urlparse import urlparse, urljoin

class CrawlerSource(object):
        def __init__(self, origin_url):
            self.origin_url = origin_url
            self.visit_queue = [origin_url]
            self.visited_urls = []
            self.domain = urlparse(origin_url).netloc

        def __iter__(self):
            return self

        def next(self):
            while(True):
                if(len(self.visit_queue) <= 0):
                    raise StopIteration
                url = self.visit_queue.pop()
                if(url in self.visited_urls):
                    continue
                article = newspaper.Article(url)
                article.download()
                article.parse()

                article_urls = article.extractor.get_urls(article.doc)
                for u in article_urls:
                    u = urljoin(url, u, False)
                    if(self._should_crawl(u)):
                        self.visit_queue.append(u)
                return article

        def _should_crawl(self, url):
            parsed_url = urlparse(url)
            if(self.domain.endswith(parsed_url.netloc)):#use ends with to avoid checking subdomains like www.
                return True
            return False