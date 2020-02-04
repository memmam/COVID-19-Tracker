#!/usr/bin/python3

# 2019-nCoV Tracker v3.0-beta-1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-04
#
# A Twitter bot for posting information on the spread of the 2019-nCoV outbreak
#
# Uses Requests, Tweepy, and gspread libraries
#
# File: nCoV_twitter.py
# Purpose: Methods for nCoV.py that use Twitter API

# Import our Twitter credentials and Tweepy library from credentials.py
from credentials import *

# Get Twitter API access
def get_twitter_api():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    
    return api

# Send nCoV tweets
def output(send_flag, api, tweet_list):
    # Prepare for list output
    length = len(tweet_list)

    # Output master tweet
    print(f"\n{tweet_list[0]}")

    if send_flag == True:
        prev_tweet = api.update_status(tweet_list[0])

    # Output and post replies in list
    for i in range(1, length):
        # Test print / terminal output
        print(f"\n{tweet_list[i]}")

        # Send tweet
        if send_flag == True:
            time.sleep(5)
            prev_tweet = api.update_status("@" + prev_tweet.user.screen_name + "\n\n" + tweet_list[i], prev_tweet.id)