# Test script for debugging cron, posts a test message with a timestamp

import time
import tweepy
import requests
import json

# Import our Twitter credentials from credentials.py
from credentials import *

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
    wait_on_rate_limit_notify=True)
api = tweepy.API(auth, wait_on_rate_limit=True,

# Get current UTC time
utctime = time.gmtime()

# Build tweet string
test_tweet = """ AUTOMATED POST TEST
{utctime.tm_year}-{utctime.tm_mon}-{utctime.tm_mday} {utctime.tm_hour}:{utctime.tm_min}:{utctime.tm_sec} UTC"""

# Test print / terminal output
print(test_tweet)

# Send tweet
api.update_status(test_tweet)
