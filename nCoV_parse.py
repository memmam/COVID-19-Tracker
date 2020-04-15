#!/usr/bin/python3

# Coronavirus Disease Tracker v10.7b
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-04-15
#
# A Twitter/Discord bot for posting information on the spread of the COVID-19
# outbreak
#
# Uses Requests, Tweepy, pandas, discord-webhook, and matplotlib libraries
#
# File: nCoV_parse.py
# Purpose: Methods for parsing Johns Hopkins data

# Import nCoV-parse methods for parsing Johns Hopkins data
from nCoV_fetch import *
from nCoV_twitter import *

# Build individual report field for Discord embed
def build_discord(c_flag, c_name, diff_arr, diff_offset, jh_dict,
                  friendlyname=None):
    # Create title for field
    if friendlyname == None:
        friendlyname = c_name
    stats_label = f"{c_flag} {friendlyname}:"

    # Generate statistics figures for fields

    # Total cases
    stats_content = f"😷 {jh_dict[c_name]['Confirmed']:,}"
    # Deltas?
    if diff_arr[diff_offset + 0] != 0:
        stats_content = f"{stats_content} ({diff_arr[diff_offset]:+,})\n"
    else:
        stats_content = f"{stats_content}\n"

    # Active cases
    active_cases = \
        jh_dict[c_name]['Confirmed'] - jh_dict[c_name]['Deaths'] \
        - jh_dict[c_name]['Recovered']
    stats_content = f"{stats_content}🏥 {active_cases:,}"
    # Deltas?
    if diff_arr[diff_offset] - diff_arr[diff_offset + 1] - diff_arr \
            [diff_offset + 2] != 0:
        active_case_delta = diff_arr[diff_offset] - diff_arr[diff_offset + 1] \
            - diff_arr[diff_offset + 2]
        stats_content = f"{stats_content} ({active_case_delta:+,})\n"
    else:
        stats_content = f"{stats_content}\n"

    # Dead
    stats_content = f"{stats_content}💀 {jh_dict[c_name]['Deaths']:,}"
    # Deltas?
    if diff_arr[diff_offset + 1] != 0:
        stats_content = f"{stats_content} ({diff_arr[diff_offset + 1]:+,})\n"
    else:
        stats_content = f"{stats_content}\n"

    # Recovered
    stats_content = f"{stats_content}👍 {jh_dict[c_name]['Recovered']:,}"
    # Deltas?
    if diff_arr[diff_offset + 2] != 0:
        stats_content = f"{stats_content} ({diff_arr[diff_offset + 2]:+,})"
    else:
        stats_content = f"{stats_content}"

    return stats_label, stats_content

# Build individual reports for tweet
def build_twitter(c_flag, c_name, jh_dict, stats_twitter):
    # Total cases
    stats_twitter = f"{stats_twitter}{c_flag}😷{jh_dict[c_name]['Confirmed']:,}"
    # Active
    active_cases = jh_dict[c_name]['Confirmed'] - jh_dict[c_name]['Deaths'] \
        - jh_dict[c_name]['Recovered']
    stats_twitter = f"{stats_twitter} 🏥{active_cases:,}"
    # Dead
    stats_twitter = f"{stats_twitter} 💀{jh_dict[c_name]['Deaths']:,}"
    # Recovered
    stats_twitter = f"{stats_twitter} 👍{jh_dict[c_name]['Recovered']:,}\n"

    return stats_twitter

# Build stats tweet from requested data
def build_stats(send_flag, api, datecode, datecode_hour, hour):
    # Scrape data
    jh_dict, jh_csv_dict = get_jh()

    # Allows clock emoji in timestamps to reflect current hour
    clocks = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", \
              "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]

    # Using scraped data and config/data file, generate the following:
        # prev_arr: data as of last update
        # header_arr: config data for each country
        # curr_arr: data as of now
        # update_arr: new config/data file to be saved
    prev_arr, header_arr, curr_arr, update_arr = comp_nCoV(clocks[hour%12], \
                                                 send_flag, api, datecode, \
                                                 jh_dict)

    # Create array of deltas from last update to now
    diff_arr = []
    for i in range(len(prev_arr)):
        diff_arr.append(curr_arr[i] - prev_arr[i])

    # Choose correct world emoji for 'Worldwide' count to reflect current
    # real-world daytime
    if hour >= 23 or hour <= 7:
        globe = "🌏"
    elif hour >= 8 and hour <= 13:
        globe = "🌍"
    elif hour >= 14 and hour <= 22:
        globe = "🌎"

    # Update globe in header array based on previous
    header_arr[0] = globe

    # Create empty string to store tweet data
    stats_twitter = ""

    # Generate tweet data for the topmost five entries in config file
    for i in range(0,25,5):
        stats_twitter = build_twitter(header_arr[i], header_arr[i+1], jh_dict, \
                        stats_twitter)

    # Append emoji key footer to tweet
    stats_twitter = f"{stats_twitter}\n😷Total 🏥Active 💀Dead 👍Recovered"

    # If a webhook file exists, create Discord embed data
    try:
        with open ("webhooks.txt", "r") as webhook_file:
            webhook_file.close()

        length = len(header_arr)
        stats_discord = {}

        diff_offset = 0

        # Iterate along header data five entries at a time, creating list of
        # Discord embed fields for each entry in the config file
        for i in range(0,length,5):
            stats_label, stats_content = build_discord(header_arr[i], \
                                         header_arr[i+1], diff_arr, \
                                         diff_offset, jh_dict, friendlyname \
                                         = header_arr[i+2])
            stats_discord[stats_label] = stats_content
            diff_offset = diff_offset + 3

        # Create Discord datestamp
        date_discord = f"{clocks[hour%12]} Last Updated: {datecode}"
    except:
        stats_discord = ''
        date_discord = ''

    # Build statistics tweet
    stats_tweet = (f"{clocks[hour%12]}{datecode_hour} #COVID19 #Coronavirus\n\n"
    f"{stats_twitter}")

    return stats_tweet, stats_discord, date_discord, stats_tweet, jh_dict, \
           jh_csv_dict, header_arr, update_arr

# Generate case data based on config/data file and scraped JHU web data
def comp_nCoV(clock, send_flag, api, datecode, jh_dict):
    # Check for existence of config/data file
    try:
        with open ("config.txt", "r") as config_file:
            config_data = config_file.readlines()
            config_file.close()
    except:
        print("No config file!")
        sys.exit()

    length = len(config_data)

    # Strip newlines from config data, and convert non-string data to what it's
    # supposed to be instead of a string
    for i in range(length):
        config_data[i] = config_data[i].replace("\n", "")

        if i % 8 == 3:
            config_data[i] = int(config_data[i])
        elif i % 8 == 4:
            # Empty filter lists are often misinterpreted by the file reader.
            # I've seen three different types of erroneous reads, this
            # conditional handles all of them
            if config_data[i] != '[]' and config_data[i] != '' and \
                    config_data[i] != ['']:
                config_data[i] = list(config_data[i].split(','))
            else:
                config_data[i] = []

    # Create array of last-run case data, for use in generating deltas
    compare_data = []
    for i in range(length):
        if i % 8 > 4:
            compare_data.append(int(config_data[i]))

    # Create array of per-country metadata, for use in generating output
    header_data = []
    for i in range(length):
        if i % 8 < 5:
            header_data.append(config_data[i])

    # Create new config file dadta
    update_data = []
    length = len(header_data)
    for i in range(length):
        if i % 5 == 4:
            update_data.append(','.join(header_data[i]))
            update_data.append(jh_dict[header_data[i - 3]]['Confirmed'])
            update_data.append(jh_dict[header_data[i - 3]]['Deaths'])
            update_data.append(jh_dict[header_data[i - 3]]['Recovered'])
        else:
            update_data.append(header_data[i])

    # Create array of current case data, for use...basically everywhere
    tweet_data_arr = []
    for i in range(0, length, 5):
        tweet_data_arr.append(jh_dict[header_data[i + 1]]['Confirmed'])
        tweet_data_arr.append(jh_dict[header_data[i + 1]]['Deaths'])
        tweet_data_arr.append(jh_dict[header_data[i + 1]]['Recovered'])

    # Check if data has changed since last run; if not, abort (but only if 
    # posting an update)
    if send_flag == True:
        new_data = False
        length = len(compare_data)
        for i in range(length):
            if tweet_data_arr[i] != compare_data[i]:
                new_data = True
        if new_data == False:
            print("No new data")
            lastcheckedupdate(clock, send_flag, api, datecode)
            exit()

    return compare_data, header_data, tweet_data_arr, update_data
