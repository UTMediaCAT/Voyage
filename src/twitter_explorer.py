import db_manager
import tweepy
import time

# Twitter Developer API
CONSUMER_KEY = "UITySH5N4iGOE3l6C0YgmwHVd"
CONSUMER_SECRET = "H7lXeLBDQv3o7i4wISGJtukdAqC6X9Vr4EXTdaIAVVrN56Lwbh"
ACCESS_TOKEN = "2825329492-TKU4s0Mky7vazr60WKHQV7R6sJT2wYE4ysR3Gm3"
ACCESS_TOKEN_SECRET = "I740fF6x6v0srzbY7LCAjNWXXOzZRMBFbkoiwZ5FgqC5s"

#seconds to wait before retrying call
WAIT_RATE = (60 *1) + 0

def authorize():
    ''' (None) -> tweepy.API
    Will use global keys to allow use of API
    '''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)
    

def get_tweets(screen_name, amount):
    ''' (str, [int]) -> list of list
    Gets amount tweets from specified users
    Returns list in format [uni tweet, uni user, str time_tweeted]
    '''
    api = authorize()
    user = api.get_user(screen_name)
    
    tweets = []
    last_id = -1
    #incase user asks for more tweets than avaliable
    while len(tweets) < amount and len(tweets) != user.statuses_count:
        #check how many more tweets is needed
        count = amount - len(tweets)
        try:
            new_tweets = api.user_timeline(screen_name = screen_name,
                                       count = count)

            #If there are no more tweets, finish
            if not new_tweets:
                break
            #Add new tweets
            for tweet in new_tweets:
                tweets.append(tweet)
            last_id = tweets[-1].id

        #If limit is reached
        except tweepy.TweepError as e:
            print '=== Limit Reached ===.'
            print ('Resuming in ' + str(int(WAIT_RATE/60)) + ' minute(s) and '
                   + str(WAIT_RATE%60) + ' second(s).')
            time.sleep((15 * 60) + 10)
            continue
    return tweets

def get_follower_count(screen_name):
    ''' (str) -> int
    Gets number of followers of screen_name's account
    '''
    api = authorize()
    user = api.get_user(screen_name)
    return user.followers_count

def get_followers(screen_name):
    ''' (str) -> inicode
    Returns list of all followers (unicode string) of user screen_name

    If limit for follower calling is reached, the function will sleep and notify
    with a print statement, later continuing the call(s).
    '''
    api = authorize()
    
    followers = []
    again = False
    while True:
        try:
            for user in tweepy.Cursor(api.followers, screen_name=screen_name).items():
                followers.append(user.screen_name)
            again = False
            #if all followers are there, return
            if len(followers) == get_follower_count(screen_name):
                return followers
            
        #if call limit is reached
        except tweepy.TweepError as e:
            if not again:
                print '=== Limit Reached ===.'
            if again:
                print '=== Limit Still Not Over ===.'
            print ('Resuming in ' + str(int(WAIT_RATE/60)) + ' minute(s) and '
                   + str(WAIT_RATE%60) + ' second(s).')
            time.sleep(WAIT_RATE)
            again = True
            continue
            
            
def search_tweets(keyword, result_type, amount):
    '''(str, str, int) -> list of statuses
    Takes keyword, result_type ('mixed', 'recent', 'popular'), and amount.
    Will return tweets as status objects in a list. The number of statuses
    returned deprends on how many are found and/or the predetermined amount
    requested

    If limit for tweet calling is reached, the function will sleep and notify
    with a print statement, later continuing the call(s).

    #NOTE: If any status update data includes keyword, or if the link included
    in the status contains the keyword that tweet will be used.
    '''
    api = authorize()
    
    tweets = []
    last_id = -1
    while len(tweets) < amount:
        #check how many more tweets is needed
        count = amount - len(tweets)
        try:
            new_tweets = api.search(q=keyword, count=count,
                                    result_type = result_type,lang='en',
                                    max_id=str(last_id - 1),
                                    show_user = True)

            #If there are no more tweets, finish
            if not new_tweets:
                break
            #Add new tweets
            for tweet in new_tweets:
                tweets.append(tweet)
            last_id = tweets[-1].id

        #If limit is reached
        except tweepy.TweepError as e:
            print '=== Limit Reached ===.'
            print ('Resuming in' + str(int(WAIT_RATE/60)) + ' minute(s) and '
                   + str(WAIT_RATE%60) + ' second(s).')
            time.sleep((15 * 60) + 10)
            continue
    return tweets

def add_tweet():
    pass

            

if __name__ == '__main__':
    #pass in the username of the account you want to download
    for tweet in get_tweets('acmeteam',2):
        print tweet.text

    print '============================='
    
    for user in get_followers('acmeteam4'):
        print user

    print '============================='
    
    print get_follower_count('apple')

    print '============================='
    
    test_search = search_tweets('acme', 'recent', 5)
    
    for tweet in test_search:
        print tweet.user.screen_name
        print tweet.text
        print ('------------')
