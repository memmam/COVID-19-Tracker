#!/usr/bin/python3

# 2019-nCoV Tracker v3.2-beta
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-06
#
# A Twitter bot for posting information on the spread of the 2019-nCoV outbreak
#
# Uses Requests, Tweepy, and gspread libraries
#
# File: nCoV_parse.py
# Purpose: Methods for parsing Johns Hopkins data

# Import nCoV-parse methods for parsing Johns Hopkins data
from nCoV_sheets import *

# Import nCoV-parse methods for parsing Johns Hopkins data
from nCoV_fetch import *

# Build stats tweet from requested data
def build_stats_tweet(send_flag, datecode):
    # request header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    # scrapers
    qq_total, qq_suspect, qq_recovered, qq_dead = get_qq(headers)
    jh_total, jh_dead, jh_recovered = get_jh(headers)

    if send_flag == True:
        # Collect tweet data as string for abort script in next line
        tweet_data = (f"{jh_total}\n"
        f"{jh_dead}\n"
        f"{jh_recovered}\n"
        f"{qq_total}\n"
        f"{qq_suspect}\n"
        f"{qq_dead}\n"
        f"{jh_recovered}")

        abort_flag = abort_nCoV(tweet_data)

        if abort_flag == True:
            return "ABORT"

    # Construct statistics
    stats = (f"{jh_total:,} (JH) / {qq_total:,} (QQ) cases\n"
    f"{qq_suspect:,} (QQ) suspected\n"
    f"{jh_dead:,} (JH) / {qq_dead:,} (QQ) deaths\n"
    f"{jh_recovered:,} (JH) / {qq_recovered:,} (QQ) recoveries\n\n"
    "JH = Johns Hopkins\n"
    "QQ = QQ News")
    
    # Define footer
    try:
        with open ("footer.txt", "r") as hash_file:
            footer=hash_file.read()
            hash_file.close()
    except:
        footer=""

    # Build statistics tweet
    stats_tweet = (f"{datecode}\n\n"
    f"{stats}")

    if footer != "":
        stats_tweet = (f"{stats_tweet}\n\n"
        f"{footer}")

    return stats_tweet

def abort_nCoV(tweet_data):
    # If no new data, abort
    try:
        with open ("prev_nums.txt", "r") as tweet_file:
            last_tweet_data = tweet_file.readlines()
            tweet_file.close()
            
        length = len(last_tweet_data)

        for i in range(length):
            last_tweet_data[i] = int(last_tweet_data[i].replace('\n', ''))

        tweet_data_arr = tweet_data.split('\n')
        length = len(tweet_data_arr)

        for i in range(length):
            tweet_data_arr[i] = int(tweet_data_arr[i])

        with open ("prev_nums.txt", "w") as tweet_file:
            tweet_file.write(tweet_data)
            tweet_file.close()

        if last_tweet_data == tweet_data_arr:
            print("No new data")
            return True
    except:
        with open ("prev_nums.txt", "w") as tweet_file:
            tweet_file.write(tweet_data)
            tweet_file.close()

    return False

# Parser for JH spreadsheet
def parse_jh(jh_worksheet_list):
    length = len(jh_worksheet_list)
    countries_list = []
    jh_processed_data = {}

    # Core parser logic

    # Iterate over sheet
    for i in range(length):
        # If a given country is already in the processed data, append the province to it
        if jh_worksheet_list[i].get('Country/Region') not in countries_list:
            countries_list.append(jh_worksheet_list[i].get('Country/Region'))
            jh_processed_data[jh_worksheet_list[i].get('Country/Region')] = {
                    'province_data': {jh_worksheet_list[i].get('Province/State'): [jh_worksheet_list[i].get('Confirmed'),  jh_worksheet_list[i].get('Deaths'),  jh_worksheet_list[i].get('Recovered'),  jh_worksheet_list[i].get('Last Update')]},
                    'total_confirmed': jh_worksheet_list[i].get('Confirmed'),
                    'total_dead': jh_worksheet_list[i].get('Deaths'),
                    'total_recovered': jh_worksheet_list[i].get('Recovered')
                }
        
        # Else, create a new country entry in the processed data, and populate it with the current province
        else:
            country_index = countries_list.index(jh_worksheet_list[i].get('Country/Region'))
            jh_country = jh_processed_data[jh_worksheet_list[i].get('Country/Region')]

            jh_country['province_data'][jh_worksheet_list[i].get('Province/State')] = [jh_worksheet_list[i].get('Confirmed'), jh_worksheet_list[i].get('Deaths'),  jh_worksheet_list[i].get('Recovered'), jh_worksheet_list[i].get('Last Update')] 
            jh_country['total_confirmed'] = jh_country['total_confirmed'] + jh_worksheet_list[i].get('Confirmed')
            jh_country['total_dead'] = jh_country['total_dead'] + jh_worksheet_list[i].get('Deaths')
            jh_country['total_recovered'] = jh_country['total_recovered'] + jh_worksheet_list[i].get('Recovered')

    return jh_processed_data

# Get and parse Johns Hopkins CSSU data
def get_parse_jh():
    jh_worksheet = get_jh_worksheet()

    # Catch failed spreadsheet load
    if jh_worksheet == 0:
        return 0

    jh_worksheet_list = jh_worksheet.get_all_records()

    jh_parsed_data = parse_jh(jh_worksheet_list)

    return jh_parsed_data

# Load historical spreadsheet data
def load_historical(load_flag, jh_parsed_data):
    # Load spreadsheet JSON
    try:
        with open ("jh_sheet.json", "r") as json_file:
            historical_data = json.load(json_file)
            json_file.close()
    except:
        with open ("jh_sheet.json", "w") as json_file:
            json.dump(jh_parsed_data, json_file)
            json_file.close()
        with open ("jh_sheet.json", "r") as json_file:
            historical_data = json.load(json_file)
            json_file.close()

    return historical_data

# Build replies from processed data
def build_replies(load_flag, datecode):

    jh_parsed_data = get_parse_jh()

    historical_data = load_historical(load_flag, jh_parsed_data)

    # Catch failed spreadsheet load
    if jh_parsed_data == 0:
        return []

    # print(jh_parsed_data)

    return []