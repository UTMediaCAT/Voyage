__author__ = 'Kyle'

import sys
sys.path.append("..")

import twitter_explorer as te
import unittest
import tweepy


class TestTwitterExplorer(unittest.TestCase):

    def setUp(self):
        self.test_account = 'acmeteam4'
        self.test_keywords = ['nevereverthere', '.ly', '.com', 'test', 'acme4', '6', '3', '2', 'google', 'time', 'no']
        self.test_sources = ['http://google.com', 'google.com','http://cnn.com', 'http://time.com', 'http://rapgenius.com/President']
    
    def tearDown(self):
        self.test_account = None
        self.test_keywords = None
        self.test_sources = None

    def testAuthorizeTwitterDeveloperAPI(self):
        """
        testing authorization of twitter development keys into tweepy.api
        """
        authorize = te.authorize()
        self.assertIsInstance(authorize, tweepy.API,
                              'Authorize() is not returning as a tweepy.API')

        #This assertion will easily eat up the Tweepy Limit Rate (Comment out if
        #causing trouble.
        self.assertTrue(authorize.verify_credentials(),
                       'Authorization was not sucessful)')

    def testGetTweetsFromScreenName(self):
        """
        testing if tweets are successfully gathers from specified user with specified amount
        """
        three_tweets = te.get_tweets(self.test_account, 3)
        five_tweets = te.get_tweets(self.test_account, 5)

        #test account only has 5 tweets
        eleven_requested_tweets = te.get_tweets(self.test_account, 11)
        
        self.assertEquals(len(three_tweets), 3,
                          'request for 3 tweets did not return 3 tweets')
        self.assertEquals(len(five_tweets), 5,
                          'request for 5 tweets did not return 5 tweets')
        self.assertEquals(len(eleven_requested_tweets), 8,
                          'request for an amount of tweets over ' +
                          'the accounts tweet number failed')

        self.assertEquals(three_tweets[0].text, 'testacme4',
                          'request for 3 tweets returned invalid tweet')
        self.assertEquals(three_tweets[1].text, 'testacme3',
                          'request for 3 tweets returned invalid tweet')
        self.assertEquals(three_tweets[2].text, 'testacme2',
                          'request for 3 tweets returned invalid tweet')
        
        self.assertEquals(five_tweets[0].text, 'testacme4',
                          'request for 5 tweets returned invalid tweet')
        self.assertEquals(five_tweets[1].text, 'testacme3',
                          'request for 5 tweets returned invalid tweet')
        self.assertEquals(five_tweets[2].text, 'testacme2',
                          'request for 5 tweets returned invalid tweet')
        self.assertEquals(five_tweets[3].text, 'testacme1',
                          'request for 5 tweets returned invalid tweet')
        self.assertEquals(five_tweets[4].text, 'testacme0',
                          'request for 5 tweets returned invalid tweet')

        self.assertEquals(five_tweets[0].id, 531976729007771648,
                          'tweet did no have correct id')
        self.assertEquals(five_tweets[1].id, 531976714730364929,
                          'tweet did not have correct id')
        self.assertEquals(five_tweets[2].id, 531976696397070336,
                          'tweet did not have correct id')
        self.assertEquals(five_tweets[3].id, 531976682128031744,
                          'tweet did not have correct id')
        self.assertEquals(five_tweets[4].id, 531976660015652864,
                          'tweet did not have correct id')

        for tweet in five_tweets:
            self.assertEquals(tweet.user.screen_name, 'acmeteam4',
                          'tweet was not taken from the correct user')

        for tweet in five_tweets:
            self.assertIsInstance(tweet, tweepy.Status,
                                    'Should be returning list of tweepy statuses, but is not')

    def testGetFollowerCount(self):
        """
        Tests if get_followers returns an integer and is the correct amount of followers
        """
        acme_followers = te.get_follower_count('acmeteam4')
        apple_followers = te.get_follower_count('apple')

        self.assertIsInstance(acme_followers, int,
                              "get_follower_count is not returning an int")
        self.assertIsInstance(apple_followers, int,
                              "get_follower_count is not returning an int")
        self.assertNotEquals(acme_followers, apple_followers,
                             "get_follower_count is returning same result for @acmeteam4 and @apple" +
                             "which is most likely incorrect.")

    def testGetKeywords(self):
        """
        Tests to see if correct keywords are gathered from specified tweets
        """
        eight_tweets = te.get_tweets(self.test_account, 8)
        holder = {}
        
        for tweet in eight_tweets:
            matched = te.get_keywords(tweet, self.test_keywords)
            holder.update({tweet.id : matched})
            self.assertIsInstance(matched, list,
                              'Not returing list of matched keywords')
        
        print holder
        expected = {531976714730364929: ['test', '3'],
                    531976454138241024: ['.ly', '.com', '3', 'google', 'no'],
                    531976660015652864: ['test'],
                    531976682128031744: ['test'],
                    531976729007771648: ['test', 'acme4'],
                    531976696397070336: ['test', '2'],
                    531976627870527488: ['.com', 'google'],
                    531975600152805376: ['.com', 'test', '2', 'google', 'time', 'no']}

        self.assertEquals(holder, expected,
                          'Not returning correct list of keywords for each test tweet.')

        holder = {}
        for tweet in eight_tweets:
            matched = te.get_keywords(tweet, [])
            holder.update({tweet.id : matched})

        expected = {531976714730364929: [],
                    531976454138241024: [],
                    531976660015652864: [],
                    531976682128031744: [],
                    531976729007771648: [],
                    531976696397070336: [],
                    531976627870527488: [],
                    531975600152805376: []}
        
        self.assertEquals(holder, expected,
                          'Not returning empty list when no keywords are selected.')

    def testGetSources(self):
        """
        Tests to see if correct sources are gathered from specified tweets
        """
        eight_tweets = te.get_tweets(self.test_account, 8)
        holder = {}
        
        for tweet in eight_tweets:
            matched = te.get_sources(tweet, self.test_sources)
            holder.update({tweet.id : matched})
            self.assertIsInstance(matched, list,
                              'Not returing list of matched keywords')
        print holder
        expected= {531976714730364929: [],
                   531976454138241024: [],
                   531976660015652864: [],
                   531976682128031744: [],
                   531976729007771648: [],
                   531976696397070336: ['http://cnn.com'],
                   531976627870527488: ['http://cnn.com', "http://rapgenius.com/"],
                   531975600152805376: ['http://google.com',
                                         'http://cnn.com', 'http://time.com']}

        self.assertEquals(holder, expected,
                          'Not returning correct list of keywords for each test tweet.')

        holder = {}
        for tweet in eight_tweets:
            matched = te.get_sources(tweet, [])
            holder.update({tweet.id : matched})

        expected = {531976714730364929: [],
                    531976454138241024: [],
                    531976660015652864: [],
                    531976682128031744: [],
                    531976729007771648: [],
                    531976696397070336: [],
                    531976627870527488: [],
                    531975600152805376: []}
        
        self.assertEquals(holder, expected,
                          'Not returning empty list when no sources are selected.')
        
    def testStressGetTweets(self):
        """
        Tests to see if twitter_explorer handles that rate call correctly, and completes task
        """
        holder = []
        i = 0
        count = 0
        while i < 1000:
            holder.append(te.get_tweets('acmeteam4', 1))
            i +=1#        for tweets in holder:
            count += 1

        self.assertEquals(count, 1000, 'getting amount of tweets over rate limit failed')
if __name__ == '__main__':
    unittest.main()
