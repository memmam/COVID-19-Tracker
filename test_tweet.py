#!/usr/bin/python3

# 2019-nCoV Tracker v3.0-beta-3
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-05
#
# A Twitter bot for posting information on the spread of the 2019-nCoV outbreak
#
# Uses Requests, Tweepy, and gspread libraries
#
# File: test_tweet.py
# Purpose: Test driver for Twitter API access

# Import for UTC datestamp
import time

# Import Tweepy for Twitter API access
import tweepy

# Import Twitter API getter method from nCoV_twitter 
from nCoV_twitter import get_twitter_api

def main():
    # Get current UTC time
    utctime = time.gmtime()

    # Get API access
    api = get_twitter_api()

    # Build tweet string
    test_tweet = (f"AUTOMATED POST TEST\n"
    f"{utctime.tm_year:04}-{utctime.tm_mon:02}-{utctime.tm_mday:02} {utctime.tm_hour:02}:{utctime.tm_min:02}:{utctime.tm_sec:02} UTC")

    # Test print / terminal output
    print(test_tweet)

    # Send tweet
    api.update_status(test_tweet)

if __name__ == "__main__":
    main()