#!/usr/bin/python3

# Coronavirus Disease Tracker v6.0-b
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-03-22
#
# A Twitter bot for posting information on the spread of the COVID-19 outbreak
#
# Uses Requests, Tweepy, and pandas libraries
#
# File: nCoV.py
# Purpose: Main driver for Coronavirus Disease Tracker

# Import for command line arguments
import argparse

# Import nCoV_twitter methods (also imports time, credentials, and Tweepy)
from nCoV_twitter import *

# Import nCoV_parse methods (also imports nCoV_fetch methods, Requests, and json)
from nCoV_parse import *

# Import CSV processing methods
from nCoV_csv import *

# Main method
def main():
    # Command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--notweet', help='Do not post a tweet', action="store_true")
    parser.add_argument('--verbose', help='Turn on verbose output', action="store_true")
    args = parser.parse_args()
    
    if args.notweet:
        print("Notweet mode on.")
    if args.verbose:
        print("Verbose mode on.")
    
    # Get API access
    api = get_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)

    # Get current UTC time
    utctime = time.gmtime()
    datecode = f"{utctime.tm_year:04}-{utctime.tm_mon:02}-{utctime.tm_mday:02} {utctime.tm_hour:02}:{utctime.tm_min:02} UTC"
    datecode_hour = f"{utctime.tm_year:04}-{utctime.tm_mon:02}-{utctime.tm_mday:02} {utctime.tm_hour:02}H UTC"

    # Build stats tweet, get csv data
    stats_tweet, stats_discord, date_discord, nCoV_data, jh_total_csv, jh_dead_csv, jh_recovered_csv = build_stats(not args.notweet, api, datecode, datecode_hour, utctime.tm_hour)

    # Generate graphs
    allcountries_graph, china_graph, not_china_graph = generate_graphs(jh_total_csv, jh_dead_csv, jh_recovered_csv)

    # Send main tweet
    output(not args.notweet, api, [stats_tweet], stats_discord, date_discord, nCoV_data, datecode, utctime.tm_hour)

    if args.verbose:
        # Get API keys for second Twitter account if one exists, else default to the main Twitter account
        try:
            api_verbose = get_twitter_api(consumer_key_verbose, consumer_secret_verbose, access_token_verbose, access_token_secret_verbose)
        except:
            api_verbose = api

        tweet_arrays = build_verbose(not args.notweet, datecode, datecode_hour, utctime.tm_hour)

        arr_length = len(tweet_arrays)

        tweet_sum = 0

        for i in range(arr_length):
            tweet_sum += len(tweet_arrays[i])

        for i in range(arr_length):
            if tweet_sum < 100:
                output(not args.notweet, api_verbose, tweet_arrays[i])
            else:
                output(not args.notweet, api_verbose, [tweet_arrays[i][0]])

# Start main method
if __name__ == "__main__":
    main()