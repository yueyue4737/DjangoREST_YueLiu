# !/usr/bin/env/python3
# Copyright 2019 YueLiu liuyue2@bu.edu
# Program Goal: get three dataset-- the real-time, the published and the sentiment score

# import libraries
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account
import json
import numpy as np
import os
import pandas as pd
import tweepy

# credentials
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
credentials_path = os.path.dirname(os.path.realpath(__file__)) + os.sep + "FILENAME.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# authentication
# create an OAuthHandler instance
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# re-build the OAuthHandler from the stored access token
auth.set_access_token(access_token, access_token_secret)
client = language.LanguageServiceClient(credentials=credentials)

# Program1: getting the public tweets
def get_public_tweets(api,user,n):
    """get public tweets"""
    public_tweets = []
    # blocked when using home_timeline
    # user_timeline can help us get the specified tweets
    target = tweepy.Cursor(api.user_timeline, id=user)
    for tweet in target.items(n):
        public_tweets.append(tweet)
    return public_tweets

def get_relationship(api,user):
    """get retweeters, friends lists and followers"""
    friends_list = []
    friends = api.friends(id=user)
    for i in friends:
        friends_list.append(i)
    followers_list = []
    followers = api.followers(id=user)
    for j in followers:
        followers_list.append(j)
    return friends_list, followers_list

def get_retweets(self, id):
    """require the numeric id"""
    retweets = self.api.retweet(id)
    return retweets

# Program2: getting the real-time tweets
class StdOutListener(tweepy.StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        with open("streaming.json", 'w') as f:
            f.write(data)
        return True

    def on_error(self, status):
        print(status)

# Program3: analyzing the sentiment of the tweets
def sentiment_analysis(text):
    """
    Sentiment Analysis by using Google Natural Language API
    """
    # content for analysis
    # sentiment analysis by the basic methods
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return sentiment.score

if __name__ == '__main__':
    # the menu
    print("Hit control-z when you want to terminate the streaming!")
    # get the published tweet dataset
    api = tweepy.API(auth)
    user = 'NationalVOAD'
    tweets = get_public_tweets(api, user, 200)
    published_df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    published_df['id'] = np.array([tweet.id for tweet in tweets])
    published_df['keyword'] = np.array([tweet.id for tweet in tweets])
    published_df['location'] = np.array([tweet.id for tweet in tweets])
    published_df['text'] = np.array([tweet.id for tweet in tweets])
    published_df['target'] = np.array([tweet.id for tweet in tweets])
    published_df.to_csv('published_tweet.csv')
    # get the sentiment data set
    score = []
    for i in tweets:
        score_i = sentiment_analysis(i.text)
        score.append(score_i)
    sentiment_df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    sentiment_df['sentiment'] = np.array([score])
    # get the real-time data set
    my_listener = StdOutListener()
    stream = tweepy.Stream(auth, my_listener)
    # amend the word list in mini project 2
    stream.filter(track=["Earthquake", "aftershock", "Hurricane", "wildfires", "HillsideFire", "burn", "tides", "storm", "flood",
               "lightning", "Tropical"])
