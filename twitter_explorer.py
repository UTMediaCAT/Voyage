import db_manager
import tweepy

# Twitter Developer API
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

    
def get_recent_tweets(user, amount=20):
    ''' (str, [int]) -> list of list
    Gets amount tweets from specified users
    Returns list in format [uni tweet, uni user, str time_tweeted]
    '''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    new = api.user_timeline(screen_name = user, count = amount)

    tweet_list = []

    for tweet in new:
        tweet_list.append([tweet.text ,tweet.user.screen_name ,str(tweet.created_at)])
    print tweet_list

def get_followers(user):
    ''' (str) -> list
    Gets usernames of all the twitter accounts following user
    Returns list in format [int followers, [list of followers]]
    '''

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    followers = []
    count = 0
    for user in tweepy.Cursor(api.followers, screen_name=user).items():
        count += 1
        followers.append(user.screen_name)
    return [count, followers]
