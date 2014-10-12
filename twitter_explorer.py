import db_manager
import tweepy

# Twitter Developer API
CONSUMER_KEY = "UITySH5N4iGOE3l6C0YgmwHVd"
CONSUMER_SECRET = "H7lXeLBDQv3o7i4wISGJtukdAqC6X9Vr4EXTdaIAVVrN56Lwbh"
ACCESS_TOKEN = "2825329492-TKU4s0Mky7vazr60WKHQV7R6sJT2wYE4ysR3Gm3"
ACCESS_TOKEN_SECRET = "I740fF6x6v0srzbY7LCAjNWXXOzZRMBFbkoiwZ5FgqC5s"

    
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

def test_search(keyword):
    holder = []
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.A4PI(auth)
    
    follower=[]
    
    for tweet in tweepy.Cursor(api.search, q = keyword, result_type = "recent",
                               include_entities=True,lang="en").items(5):
        print tweet.user.screen_name + ": " +tweet.text + "\n"
        #follower.append(tweet.user.screen_name)
    
    #for follow in follower:
        #get_followers(follow)[0]
        
        

