#!/usr/bin/env/python3

# Coronavirus Disease Tracker v10.6
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-04-13
#
# A Twitter/Discord bot for posting information on the spread of the COVID-19
# outbreak
#
# Uses Requests, Tweepy, pandas, discord-webhook, and matplotlib libraries
#
# File: nCoV.py
# Purpose: Main driver for Coronavirus Disease Tracker

# Import for command line arguments
import argparse

# Import nCoV_twitter methods (also imports time, credentials, and Tweepy)
from nCoV_twitter import *

# Import nCoV_parse methods (also imports nCoV_fetch methods, Requests, and
# json)
from nCoV_parse import *

# Import CSV processing methods
from nCoV_csv import *

# Main method
def main():
    # Command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--notweet', help='Do not post a tweet', \
                        action="store_true")
    args = parser.parse_args()

    if args.notweet:
        print("Notweet mode on.\n")

    # Get API access
    api = get_twitter_api(consumer_key, consumer_secret, access_token, \
                          access_token_secret)

    # Get current UTC time
    utctime = time.gmtime()
    datecode = (
        f"{utctime.tm_year:04}-{utctime.tm_mon:02}-{utctime.tm_mday:02} "
        f"{utctime.tm_hour:02}:{utctime.tm_min:02} UTC")
    datecode_hour = (f"{utctime.tm_mon:02}/{utctime.tm_mday:02} "
                     f"{utctime.tm_hour:02}H")

    # Build stats tweet, get csv data
    stats_tweet, stats_discord, date_discord, nCoV_data, jh_dict, jh_csv_dict, \
    header_arr, update_arr = build_stats(not args.notweet, api, datecode, \
                             datecode_hour, utctime.tm_hour)

    # Generate graphs
    generate_graphs(jh_csv_dict, jh_dict, header_arr)

    # Send main tweet
    output(not args.notweet, api, stats_tweet, stats_discord, date_discord, \
           nCoV_data, datecode, utctime.tm_hour, update_arr)

# Start main method
if __name__ == "__main__":
    main()
