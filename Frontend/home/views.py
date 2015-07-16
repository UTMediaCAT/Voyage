from django.shortcuts import render, redirect
from django.template import RequestContext, loader

def index(request):
	content = {}

	if (request.path in ["/statistics_articles",
						 "/statistics_tweets"]):
		content["statistics"] = "active"
		content[request.path[1:]] = "active"

	elif (request.path in ["/article_sourcesite",
						   "/article_keyword",
						   "/article_weighted",
						   "/article_movable",
						   "/tweet_sourcesite",
						   "/tweet_keyword",
						   "/tweet_weighted",
						   "/tweet_movable"]):
		content["visualizations"] = "active"
		content[request.path[1:]] = "active"

	elif (request.path in ["/downloads", "/contact"]):
		content[request.path[1:]] = "active"

	else:
		content["overview"] = "active"

	return render(request, 'home/index.html', content)