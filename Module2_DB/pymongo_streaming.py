# !/usr/bin/env/python3
# Copyright 2019 YueLiu liuyue2@bu.edu
# Program Goal: import the streaming dataset and summary the statistical features
# system environment: MongoDB 4.2 Community Edition for macOS

# import libraries
import json
import pymongo
from pymongo import MongoClient

# task1: import the .json file
client = MongoClient('localhost', 27017) # by default
db = client.streamingtweets
tweets = db.files
with open('PATH+FILENAME.json') as f:
    file_data = json.load(f)
tweets.insert_one(file_data) # for python 3.7, you can also insert many

# task2: summary the features of the dataset
tcol_names = client.streamingtweets.list_collection_names()
print(tcol_names)
criteria = { "Tweets": {"$exists": False}}
n_tweets = db.streamingtweets.count_documents(criteria)
print(n_tweets)
