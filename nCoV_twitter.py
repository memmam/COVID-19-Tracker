#!/usr/bin/python3

# Coronavirus Disease Tracker v4.2-b1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-03-19
#
# A Twitter bot for posting information on the spread of the COVID-19 outbreak
#
# Uses Requests, Tweepy, and pandas libraries
#
# File: nCoV_twitter.py
# Purpose: Methods for nCoV.py that use Twitter API

# Import our Twitter credentials and Tweepy library from credentials.py
from credentials import *
import time
import random

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
def output(send_flag, api, tweet_list, tweet_data, datecode, hour):

    clocks = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]

    # Prepare for list output
    length_i = len(tweet_list)

    # Output master tweet
    print(f"\n{tweet_list[0]}")

    # Send master tweet
    if send_flag == True:
        for attempt_no in range(1,3):
            try:
                master_tweet = api.update_with_media("corona.png",status=tweet_list[0])
                with open ("prev_nums.txt", "w") as tweet_file:
                    tweet_file.write(tweet_data)
                    tweet_file.close()
                break
            except:
                if attempt_no <= 3:
                    print("Retrying")
                    sleep(random.randint(15,30))
                else:
                    raise error
        lastcheckedupdate(clocks[hour], send_flag, api, datecode)

    iterations = 0
    sec_ctr = 0

    # Output and post replies in list
    for i in range(1, length_i):
        sleep_secs = random.randint(20,36)
        iterations = iterations + 1
        sec_ctr = sec_ctr + (sleep_secs)
        time.sleep(sleep_secs)

        if(iterations == 25 and sec_ctr < 900):
            sleep(900 - sec_ctr)
            sec_ctr = 0
            iterations = 0

        # Test print / terminal output
        print(f"\n{tweet_list[i]}")

        # Send tweets
        if send_flag == True:
            for attempt_no in range(1,3):
                try:
                    master_tweet = api.update_status("@" + master_tweet.user.screen_name + "\n\n" + tweet_list[i], master_tweet.id)
                except:
                    if attempt_no <= 3:
                        print("Retrying")
                        sleep(random.randint(15,30))
                    else:
                        raise error
            lastcheckedupdate(clocks[hour], send_flag, api, datecode)

def lastcheckedupdate(clock, send_flag, api, datecode):
    lastupdated = f"{clock} Updated {datecode}"

    # Define footer
    try:
        with open ("bio_top.txt", "r") as top_file:
            bio_top=top_file.read()
            top_file.close()
    except:
        bio_top=""

    try:
        with open ("bio_bottom.txt", "r") as bottom_file:
            bio_bottom=bottom_file.read()
            bottom_file.close()
    except:
        bio_bottom=""

    if bio_top != "":
        bio = (f"{bio_top}\n"
        f"{lastupdated}")
    
    if bio_bottom != "":
        bio = (f"{bio}\n"
        f"{bio_bottom}")
    
    if send_flag == True:
        for attempt_no in range(1,3):
            try:
                api.update_profile(description=bio)
            except:
                if attempt_no <= 3:
                    print("Retrying")
                    sleep(random.randint(15,30))
                else:
                    raise error

    print(bio)