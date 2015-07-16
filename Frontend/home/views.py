from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from explorer.models import Keyword as ExplorerKeyword

def index(request):
	visualizations_dict = {"/article_sourcesite": "article_hypertree",
						   "/article_keyword": "article_spacetree",
						   "/article_weighted": "article_weightedtree",
						   "/article_movable": "article_forcegraph",
						   "/tweet_sourcesite": "tweet_hypertree",
						   "/tweet_keyword": "tweet_spacetree",
						   "/tweet_weighted": "tweet_weightedtree",
						   "/tweet_movable": "tweet_forcegraph"}
	content = {}

	if (request.path in ["/statistics_articles",
						 "/statistics_tweets"]):
		content["statistics"] = "active"
		content[request.path[1:]] = "active"

	elif (request.path in visualizations_dict.keys()):
		content["visualizations"] = "active"
		content[request.path[1:]] = "active"
		content["result"] = visualizations_dict[request.path]

	elif (request.path in ["/downloads", "/contact"]):
		content[request.path[1:]] = "active"

	else:
		keyword_objs = ExplorerKeyword.objects.all()
		keywords = []

		for keyword in keyword_objs:
			keywords.append(keyword.name)

		content["keywords"] = keywords
		content["overview"] = "active"

	return render(request, 'home/index.html', content)