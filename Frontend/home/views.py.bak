from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from explorer.models import *

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

	elif (request.path in ["/downloads", "/overview"]):
		content[request.path[1:]] = "active"

	else:
		content["about"] = "active"

		rsite_objs = ReferringSite.objects.all()
		rsites = []

		for rsite in rsite_objs:
			rsites.append(rsite.url)

		content["rsites"] = rsites

		rtwitter_objs = ReferringTwitter.objects.all()
		rtwitters = []

		for rtwitter in rtwitter_objs:
			rtwitters.append(rtwitter.name)

		content["rtwitters"] = rtwitters

		ssite_objs = SourceSite.objects.all()
		ssites = []

		for ssite in ssite_objs:
			ssites.append(ssite.url)

		content["ssites"] = ssites

		stwitter_objs = SourceTwitter.objects.all()
		stwitters = []

		for stwitter in stwitter_objs:
			stwitters.append(stwitter.name)

		content["stwitters"] = stwitters

		keyword_objs = Keyword.objects.all()
		keywords = []

		for keyword in keyword_objs:
			keywords.append(keyword.name)

		content["keywords"] = keywords

	return render(request, 'home/index.html', {})



def about(request):
	return render(request, 'home/about.html', {})

def services(request):
	return render(request, 'home/services.html', {})

def faq(request):
	return render(request, 'home/faq.html', {})

def contact(request):
	return render(request, 'home/contact.html', {})
