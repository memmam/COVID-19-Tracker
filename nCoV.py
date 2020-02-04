#!/usr/bin/python3

# 2019-nCoV Tracker v3.0-beta-1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-04
#
# A Twitter bot for posting information on the spread of the 2019-nCoV outbreak
#
# Uses Requests, Tweepy, and gspread libraries
#
# File: nCoV.py
# Purpose: Main driver for 2019-nCoV Tracker

# Import for command line arguments
import argparse

# Import for UTC datestamp
import time

# Import nCoV-twitter methods (also imports credentials and Tweepy)
from nCoV_twitter import *

# Import nCoV-fetch methods (also imports Requests and json)
from nCoV_fetch import *

# Import nCoV-gsheets methods (also imports gspread and pickle)
from nCoV_gsheets import *

# Main method
def main():
    # Command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--notweet', help='Do not post a tweet', action="store_true")
    parser.add_argument('--nopickle', help='Do not update local spreadsheet object', action="store_true")
    args = parser.parse_args()
    
    if args.notweet:
        print("Notweet mode on.")
    if args.nopickle:
        print("Nopickle mode on.")
    
    # Get API access
    api = get_twitter_api()

    # Get current UTC time
    utctime = time.gmtime()
    datecode = f"{utctime.tm_year:04}-{utctime.tm_mon:02}-{utctime.tm_mday:02} {utctime.tm_hour:02}:{utctime.tm_min:02} UTC"
 
    # Create tweet list
    tweet_list = []

    # Build stats tweet and add to list
    stats_tweet = build_stats_tweet(datecode)
    tweet_list.extend([stats_tweet])

    replies = build_replies(datecode)

    # Send tweets
    output(not args.notweet, api, tweet_list)

# Start main method
if __name__ == "__main__":
    main()