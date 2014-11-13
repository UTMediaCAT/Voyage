import db_manager as db
import datetime
import tweepy
import time
import re
import urllib2
from tld import get_tld
from tld.utils import update_tld_names


__author__ = "ACME: CSCC01F14 Team 4"
__authors__ = "Yuya Iwabuchi, Jai Sughand, Xiang Wang, Kyle Bridgemohansingh, Ryan Pan"

# Twitter Developer API
CONSUMER_KEY = "UITySH5N4iGOE3l6C0YgmwHVd"
CONSUMER_SECRET = "H7lXeLBDQv3o7i4wISGJtukdAqC6X9Vr4EXTdaIAVVrN56Lwbh"
ACCESS_TOKEN = "2825329492-TKU4s0Mky7vazr60WKHQV7R6sJT2wYE4ysR3Gm3"
ACCESS_TOKEN_SECRET = "I740fF6x6v0srzbY7LCAjNWXXOzZRMBFbkoiwZ5FgqC5s"

# Globals to be used for Database
STORE_ALL_SOURCES = False
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
SITE_DB_ID = '_id'
SITE_DB_NAME = 'name'
TWEET_DB_ID = '_id'
TWEET_DB_USER = 'user'
TWEET_DB_INFLUENCE = 'store_influence'
TWEET_DB_PUBDATE = 'pub_date'
TWEET_DB_KEYWORDS = 'keywords'
TWEET_DB_SOURCES = 'sources'
TWEET_DB_STOREDATE = 'store_date'

#Seconds to wait before retrying call
WAIT_RATE = (60 * 1) + 0

def authorize():
	""" (None) -> tweepy.API
	Will use global keys to allow use of API
	"""
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	return tweepy.API(auth)

def rate_reached():
	""" (None) -> None
	Helper function to be called when a rate limit has been reached.
	"""
	print ('Twitter Rate Limit Reached, Attempting to Continue.')
	print ('Resuming in ' + str(int(WAIT_RATE/60)) + ' minute(s) and '
				   + str(WAIT_RATE % 60) + ' second(s).')
	time.sleep(WAIT_RATE)

def get_tweets(screen_name, amount):
	""" (str, [int]) -> list of list
	Gets amount tweets from specified users
	Returns list in format [uni tweet, uni user, str time_tweeted]

	Keyword arguments:
	screen_name		-- string of twitter handle
	sites           -- List of string site urls to look for
	"""
	api = authorize()
	rate_reached = True
	while rate_reached:
		try:
			user = api.get_user(screen_name)
			rate_reached = False
		except:
			rate_reached()

	tweets = []
	last_id = -1
	#incase user asks for more tweets than avaliable
	while len(tweets) < amount and len(tweets) != user.statuses_count:
		#check how many more tweets is needed
		count = amount - len(tweets)
		try:
			new_tweets = api.user_timeline(screen_name=screen_name, count=count)

			#If there are no more tweets, finish
			if not new_tweets:
				break
			#Add new tweets
			for tweet in new_tweets:
				tweets.append(tweet)
			last_id = tweets[-1].id
		except:
			rate_reached()
		return tweets



def get_follower_count(screen_name):
	""" (str) -> int
	Gets number of followers of screen_name's account

	Keyword arguments:
	screen_name		-- String of twitter handle
	"""
	api = authorize()
	while True:
		try:
			user = api.get_user(screen_name)
			return user.followers_count
		except:
			rate_reached()

def get_keywords(tweet, keywords):
	""" (status, list of str) -> list of str
	Searches and returns keywords contained in the tweet
	Returns empty list otherwise.

	Keyword arguments:
	tweet    		-- Status structre to be searched through
	sites           -- List of keywords to look for
		"""
	matched_keywords = []
	for key in keywords:
		if re.search(key, tweet.text.encode('utf8'), re.IGNORECASE):
			matched_keywords.append(key)
	return matched_keywords


def get_sources(tweet, sites):
	""" (status, list of str) -> list of str
	Searches and returns links redirected to sites within the html
	Returns empty list if none found

	Keyword arguments:
	tweet    		-- Status structre to be searched through
	sites           -- List of site urls to look for
	"""
	update_tld_names()

	matched_urls = []
	tweet_urls = []
	for url in tweet.entities['urls']:
		try:
			hold = urllib2.urlopen(url['expanded_url'])
			tweet_urls.append(get_tld(hold.geturl()))
			tweet_urls.append(url['expanded_url'])
		except:
			tweet_urls.append(get_tld(url['expanded_url']))
			continue

	# for each site, check if it exists within the urls given

	for site in sites:
		site = get_tld(site)
		if STORE_ALL_SOURCES:
			for url in tweet_urls:
				matched_urls.append(url.encode('utf8'))
			return matched_urls
		else:
			for url in tweet_urls:
				if re.search(site, url):
				# If it matches even once, append the site to the list
					matched_urls.append(url.encode('utf8'))
	# Return the list
	return matched_urls

def parse_tweets(twitter_users, keywords, foreign_sites, db_name):
	""" (list of str, list of str, list of str, str) -> none
	Parses through tweets of users, looking for keywords and foreign sites.
	Relevant tweets will be sent to a database.

	Keyword arguments:
	twitter_users   -- List of strings as twitter handles
	keywords        -- List of strings as keywords to search for
	foreign_sites   -- List of strings as sources to search for
	db_name         -- String of Database
	"""
	db.connect(db_name)
	added, updated, no_match = 0, 0, 0
	start = time.time()

	for user in twitter_users:
		print "Parsing @" + user
		tweets = get_tweets(user, 5)
		tweet_followers = get_follower_count(user)

		for tweet in tweets:
			print '\tEvaluating ...\r'
			tweet_id = tweet.id
			tweet_date = str(tweet.created_at)
			tweet_user = tweet.user.screen_name
			tweet_store_date = datetime.datetime.now().strftime(DATE_FORMAT)
			tweet_keywords = get_keywords(tweet, keywords)
			tweet_sources = get_sources(tweet, foreign_sites)

			print "\tTweet:    ", tweet.text
			print "\tAuthor:   ", tweet_user
			print "\tDate:     ", tweet_date
			print "\tKeywords: ", tweet_keywords
			print "\tSources:  ", tweet_sources
			print "\n"

			if not(tweet_keywords == [] and (tweet_sources ==[] or STORE_ALL_SOURCES)):

				try:
					db.add_document({TWEET_DB_ID: tweet_id,
					 TWEET_DB_USER:tweet_user,
					 TWEET_DB_PUBDATE: tweet_date,
					 TWEET_DB_INFLUENCE: tweet_followers,
					 TWEET_DB_STOREDATE: tweet_store_date,
					 TWEET_DB_KEYWORDS: tweet_keywords,
					 TWEET_DB_SOURCES: tweet_sources})

					added += 1
					print "\tResult:    Match detected! Added to the database."

				except:
					db.del_document(tweet_id)

					db.add_document({TWEET_DB_ID: tweet_id,
														 TWEET_DB_USER:tweet_user,
														 TWEET_DB_PUBDATE: tweet_date,
														 TWEET_DB_INFLUENCE: tweet_followers,
														 TWEET_DB_STOREDATE: tweet_store_date,
														 TWEET_DB_KEYWORDS: tweet_keywords,
														 TWEET_DB_SOURCES: tweet_sources})
					print "\tResult:    Match detected! Tweet already in database. Updating."
					updated += 1

			else:
				no_match += 1
				print "\tResult:    No Match Detected."
		print("\n\tStatistics\n\tAdded: %i | Updated: %i | No Match: %i | Time Elapsed: %is" %
		  (added, updated, no_match, time.time() - start))
		print "+--------------------------------------------------------------------+"

	print("Finished parsing all users!")
	db.close_connection()

def explore(accounts_db, keyword_db, site_db, tweet_db):
	""" (str, str, str, str) -> None
	Connects to accounts, keyword and site database, crawls within monitoring sites,
	then pushes articles which matches the keywords or foreign sites to the tweet database

	Keyword arguments:
	accounts_db         -- Twitter Accounts database name
	keyword_db          -- Keywords database name
	site_db             -- Sites database name
	tweet_db            -- Tweet database name
	"""
	while True:
		print "+----------------------------------------------------------+"
		print "| Retrieving data from Database ...                        |"
		print "+----------------------------------------------------------+"

		# Connects to Site Database
		db.connect(site_db)

		monitoring_sites = []
		# Retrieve, store, and print monitoring site information
		print "\nMonitoring Sites\n\t%-25s%-40s" % ("Name", "URL")
		for site in db.get_documents("is_monitor", True):
			# monitoring_sites is now in form [['Name', 'URL'], ...]
			monitoring_sites.append([site[SITE_DB_NAME], site[SITE_DB_ID]])
			print("\t%-25s%-40s" % (site[SITE_DB_NAME], site[SITE_DB_ID]))

		foreign_sites = []
		# Retrieve, store, and print foreign site information
		print "\nForeign Sites\n\t%-25s%-40s" % ("Name", "URL")
		for site in db.get_documents("is_monitor", False):
			# foreign_sites is now in form ['URL', ...]
			foreign_sites.append(site[SITE_DB_ID])
			print("\t%-25s%-40s" % (site['name'], site[SITE_DB_ID]))

		# Close connection with Site Database
		db.close_connection()

		# Connects to Keyword Database
		db.connect(keyword_db)
		# Retrieve all stored keywords
		keywords = db.get_all_elements()
		# Close connection with Keyord Database
		# Print all the keywords
		db.close_connection()
		print "\nKeywords:"
		for key in keywords:
			print "\t%s" % key

		print "\n"

		print "+----------------------------------------------------------+"
		print "| Populating Accounts ...                                  |"
		print "+----------------------------------------------------------+"
		# Connects to Accounts Database
		db.connect(accounts_db)
		# Retrieve all stored Accounts
		accounts = db.get_all_elements()
		for i in range(len(accounts)):
			accounts[i] = accounts[i].encode('utf8')
		# Close connection with Accounts Database
		# Print all the Accounts
		db.close_connection()
		print "\nTwitter Accounts:"
		for account in accounts:
			print "\t%s" % account

		print "\n"

		print "+----------------------------------------------------------+"
		print "| Evaluating Tweets ...                                    |"
		print "+----------------------------------------------------------+"
		# Parse the articles in all sites
		parse_tweets(accounts, keywords, foreign_sites, tweet_db)

    

if __name__ == '__main__':
	pass
	#parse_tweets(['CNN', 'TIME'], ['obama','hollywood', 'not', 'fire', 'president', 'activities'], ['http://cnn.com/', 'http://ti.me'], 'tweets')
    #explore('taccounts', 'keywords', 'sites', 'tweets')
