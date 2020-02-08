#!/usr/bin/python3

# 2019-nCoV Tracker v3.2-beta-1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-06
#
# A Twitter bot for posting information on the spread of the 2019-nCoV outbreak
#
# Uses Requests, Tweepy, and gspread libraries
#
# File: nCoV_twitter.py
# Purpose: Methods for nCoV.py that use Twitter API

# Import our Twitter credentials and Tweepy library from credentials.py
from credentials import *
import time

# Get Twitter API access
def get_twitter_api(key, secret, token, token_secret):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(token, token_secret)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    
    return api

# Send nCoV tweets
def output(send_flag, api, tweet_list):
    # Prepare for list output
    length_i = len(tweet_list)

    # Output master tweet
    print(f"\n{tweet_list[0]}")

    # Send master tweet
    if send_flag == True:
        master_tweet = api.update_with_media("corona.png",status=tweet_list[0])

    # Output and post replies in list
    for i in range(1, length_i):
        time.sleep(36)

        # Test print / terminal output
        print(f"\n{tweet_list[i]}")

        # Send tweets
        if send_flag == True:
            master_tweet = api.update_status("@" + master_tweet.user.screen_name + "\n\n" + tweet_list[i], master_tweet.id)