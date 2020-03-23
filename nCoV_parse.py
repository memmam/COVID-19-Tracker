#!/usr/bin/python3

# Coronavirus Disease Tracker v6.0-b1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-03-23
#
# A Twitter bot for posting information on the spread of the COVID-19 outbreak
#
# Uses Requests, Tweepy, and pandas libraries
#
# File: nCoV_parse.py
# Purpose: Methods for parsing Johns Hopkins data

# Import nCoV-parse methods for parsing Johns Hopkins data
from nCoV_fetch import *
from nCoV_twitter import *

# Build stats tweet from requested data
def build_stats(send_flag, api, datecode, datecode_hour, hour):
    # request header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    # scrapers
    jh_total, jh_dead, jh_recovered, jh_total_cn, jh_dead_cn, jh_recovered_cn, jh_total_csv, jh_dead_csv, jh_recovered_csv = get_jh(headers)

    # Collect tweet data as string for comp in next line
    tweet_data = (f"{jh_total}\n"
    f"{jh_total - jh_dead - jh_recovered}\n"
    f"{jh_dead}\n"
    f"{jh_recovered}\n"
    f"{jh_total_cn}\n"
    f"{jh_total_cn - jh_dead_cn - jh_recovered_cn}\n"
    f"{jh_dead_cn}\n"
    f"{jh_recovered_cn}\n")

    clocks = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]

    prev_arr, curr_arr = comp_nCoV(clocks[hour], send_flag, api, tweet_data, datecode)

    diff_arr = []

    for i in range(len(prev_arr)):
        diff_arr.append(curr_arr[i] - prev_arr[i])

    # Construct statistics for Twitter
    stats_twitter = f"☣️{jh_total:,}"
    if diff_arr[0] != 0:
        stats_twitter = f"{stats_twitter} ({diff_arr[0]:+,})\n"
    else:
        stats_twitter = f"{stats_twitter}\n"
    stats_twitter = f"{stats_twitter}🏥{jh_total - jh_dead - jh_recovered:,} active"
    if diff_arr[1] != 0:
        stats_twitter = f"{stats_twitter} ({diff_arr[1]:+,})\n"
    else:
        stats_twitter = f"{stats_twitter}\n"
    stats_twitter = f"{stats_twitter}💀{jh_dead:,} dead"
    if diff_arr[2] != 0:
        stats_twitter = f"{stats_twitter} ({diff_arr[2]:+,})\n"
    else:
        stats_twitter = f"{stats_twitter}\n"
    stats_twitter = f"{stats_twitter}✅{jh_recovered:,} recovered"
    if diff_arr[3] != 0:
        stats_twitter = f"{stats_twitter} ({diff_arr[3]:+,})"
    else:
        stats_twitter = f"{stats_twitter}"

    stats_twitter = f"{stats_twitter}\n\nOutside China:\n☣️{jh_total - jh_total_cn:,}"
    if diff_arr[0] - diff_arr[4] != 0:
        stats_twitter = f"{stats_twitter} ({diff_arr[0] - diff_arr[4]:+,})\n"
    else:
        stats_twitter = f"{stats_twitter}\n"
    stats_twitter = f"{stats_twitter}🏥{(jh_total - jh_dead - jh_recovered) - (jh_total_cn - jh_dead_cn - jh_recovered_cn):,} active"
    if diff_arr[1] - diff_arr[5] != 0:
        stats_twitter = f"{stats_twitter} ({diff_arr[1] - diff_arr[5]:+,})\n"
    else:
        stats_twitter = f"{stats_twitter}\n"
    stats_twitter = f"{stats_twitter}💀{jh_dead - jh_dead_cn:,} dead"
    if diff_arr[2] - diff_arr[6] != 0:
        stats_twitter = f"{stats_twitter} ({diff_arr[2] - diff_arr[6]:+,})\n"
    else:
        stats_twitter = f"{stats_twitter}\n"
    stats_twitter = f"{stats_twitter}✅{jh_recovered - jh_recovered_cn:,} recovered"
    if diff_arr[3] - diff_arr[7] != 0:
        stats_twitter = f"{stats_twitter} ({diff_arr[3] - diff_arr[7]:+,})"
    else:
        stats_twitter = f"{stats_twitter}"

    # Construct statistics for Discord
    try:
        with open ("webhooks.txt", "r") as webhook_file:
            webhook_file.close()
        stats_discord = f"Worldwide:\n☣️ {jh_total:,}"
        if diff_arr[0] != 0:
            stats_discord = f"{stats_discord} ({diff_arr[0]:+,})\n"
        else:
            stats_discord = f"{stats_discord}\n"
        stats_discord = f"{stats_discord}🏥 {jh_total - jh_dead - jh_recovered:,} active"
        if diff_arr[1] != 0:
            stats_discord = f"{stats_discord} ({diff_arr[1]:+,})\n"
        else:
            stats_discord = f"{stats_discord}\n"
        stats_discord = f"{stats_discord}💀 {jh_dead:,} dead"
        if diff_arr[2] != 0:
            stats_discord = f"{stats_discord} ({diff_arr[2]:+,})\n"
        else:
            stats_discord = f"{stats_discord}\n"
        stats_discord = f"{stats_discord}✅ {jh_recovered:,} recovered"
        if diff_arr[3] != 0:
            stats_discord = f"{stats_discord} ({diff_arr[3]:+,})"
        else:
            stats_discord = f"{stats_discord}"

        stats_discord = f"{stats_discord}\n\nOutside China:\n☣️ {jh_total - jh_total_cn:,}"
        if diff_arr[0] - diff_arr[4] != 0:
            stats_discord = f"{stats_discord} ({diff_arr[0] - diff_arr[4]:+,})\n"
        else:
            stats_discord = f"{stats_discord}\n"
        stats_discord = f"{stats_discord}🏥 {(jh_total - jh_dead - jh_recovered) - (jh_total_cn - jh_dead_cn - jh_recovered_cn):,} active"
        if diff_arr[1] - diff_arr[5] != 0:
            stats_discord = f"{stats_discord} ({diff_arr[1] - diff_arr[5]:+,})\n"
        else:
            stats_discord = f"{stats_discord}\n"
        stats_discord = f"{stats_discord}💀 {jh_dead - jh_dead_cn:,} dead"
        if diff_arr[2] - diff_arr[6] != 0:
            stats_discord = f"{stats_discord} ({diff_arr[2] - diff_arr[6]:+,})\n"
        else:
            stats_discord = f"{stats_discord}\n"
        stats_discord = f"{stats_discord}✅ {jh_recovered - jh_recovered_cn:,} recovered"
        if diff_arr[3] - diff_arr[7] != 0:
            stats_discord = f"{stats_discord} ({diff_arr[3] - diff_arr[7]:+,})"
        else:
            stats_discord = f"{stats_discord}"

        # Discord datestamp
        date_discord = f"{clocks[hour]} Last Updated: {datecode}"
    except:
        stats_discord = ""
        date_discord = ""

    # Define footer
    try:
        with open ("footer.txt", "r") as footer_file:
            footer=footer_file.read()
            footer_file.close()
    except:
        footer=""

    # Build statistics tweet
    stats_tweet = ("⚠️#Coronavirus Update⚠️\n\n"
    f"{clocks[hour]}{datecode_hour}\n\n"
    f"{stats_twitter}")

    if footer != "":
        stats_tweet = (f"{stats_tweet}\n\n"
        f"{footer}")

    return stats_tweet, stats_discord, date_discord, tweet_data, jh_total_csv, jh_dead_csv, jh_recovered_csv

def comp_nCoV(clock, send_flag, api, tweet_data, datecode):
    # Process data for tweet
    try:
        with open ("prev_nums.txt", "r") as tweet_file:
            last_tweet_data = tweet_file.readlines()
            tweet_file.close()
    except:
        with open ("prev_nums.txt", "w") as tweet_file:
            tweet_file.write(tweet_data)
            last_tweet_data = tweet_data.split('\n')[0:8]
            tweet_file.close()

    length = len(last_tweet_data)

    for i in range(length):
        last_tweet_data[i] = int(last_tweet_data[i].replace('\n', ''))

    tweet_data_arr = tweet_data.split('\n')[0:8]
    length = len(tweet_data_arr)

    for i in range(length):
        tweet_data_arr[i] = int(tweet_data_arr[i])

    if send_flag == True:
        if last_tweet_data == tweet_data_arr or tweet_data_arr[0] == 0 or tweet_data_arr[1] == 0 or tweet_data_arr[2] == 0 or tweet_data_arr[3] == 0 or tweet_data_arr[4] == 0 or tweet_data_arr[5] == 0 or tweet_data_arr[6] == 0 or tweet_data_arr[7] == 0:
            print("No new data")
            lastcheckedupdate(clock, send_flag, api, datecode)
            exit()

    return last_tweet_data, tweet_data_arr

# Parser for JH spreadsheet
def parse_jh(jh_worksheet_list):
    length = len(jh_worksheet_list)
    countries_list = []
    jh_processed_data = {}

    # Core parser logic

    # Iterate over sheet
    for i in range(length):
        # If a given country is not in the processed data, create a new country entry in the processed data, and populate it with the current province
        if jh_worksheet_list[i].get('Country/Region') not in countries_list:
            countries_list.append(jh_worksheet_list[i].get('Country/Region'))
            jh_processed_data[jh_worksheet_list[i].get('Country/Region')] = {
                    'province_data': {jh_worksheet_list[i].get('Province/State'): [jh_worksheet_list[i].get('Confirmed'),  jh_worksheet_list[i].get('Deaths'),  jh_worksheet_list[i].get('Recovered'),  jh_worksheet_list[i].get('Last Update')]},
                    'total_confirmed': jh_worksheet_list[i].get('Confirmed'),
                    'total_dead': jh_worksheet_list[i].get('Deaths'),
                    'total_recovered': jh_worksheet_list[i].get('Recovered')
                }
        
        # Else, append the province to it
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
    jh_worksheet = 0

    # Catch failed spreadsheet load
    if jh_worksheet == 0:
        return 0

    jh_worksheet_list = jh_worksheet.get_all_records()

    jh_parsed_data = parse_jh(jh_worksheet_list)

    return jh_parsed_data

# Load historical spreadsheet data
def load_historical(send_flag, jh_parsed_data):
    # Load spreadsheet JSON
    try:
        with open ("jh_sheet.json", "r") as json_file:
            historical_data = json.load(json_file)
            json_file.close()
        if send_flag == True:
            with open ("jh_sheet.json", "w") as json_file:
                json.dump(jh_parsed_data, json_file)
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
def build_verbose(send_flag, datecode, datecode_hour, hour):
    # List to store tweet lists
    verbose_tweets = []

    clocks = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]

    # Get spreadsheet data
    jh_parsed_data = get_parse_jh()

    # load historical data
    historical_data = load_historical(send_flag, jh_parsed_data)

    # Catch failed spreadsheet load
    if jh_parsed_data == 0:
        return []

    # Define footer
    try:
        with open ("footer_verbose.txt", "r") as footer_file:
            footer=footer_file.read()
            footer_file.close()
    except:
        footer=""

    # Lists of keys in spreadsheet data and historical spreadsheet data
    historical_keys = list(historical_data.keys())
    current_keys = jh_parsed_data.keys()

    # Keys that are new to the dataset
    new_keys = list(set(current_keys) - set(historical_keys))

    thread = []

    # Iterate across all new countries
    new_keys_length = len(new_keys)
    for i in range(new_keys_length):
        master_tweet = ("⚠️ Coronavirus Update ⚠️\n\n"
        f" {datecode}\n\n"
        f"🌐 COVID-19 spotted for the first time in {new_keys[i]}\n\n"
        f"☣️ {jh_parsed_data[new_keys[i]]['total_confirmed']:,} cases\n"
        f"💀 {jh_parsed_data[new_keys[i]]['total_dead']:,} dead\n"
        f"✅ {jh_parsed_data[new_keys[i]]['total_recovered']:,} recovered")

        if footer != "":
            master_tweet = (f"{master_tweet}\n\n"
            f"{footer}")

        thread.append(master_tweet)

        province_keys = list(jh_parsed_data[new_keys[i]]['province_data'].keys())

        province_keys_length = len(province_keys)

        # Iterate across all new states/provinces in new countries
        for j in range(province_keys_length):
            if province_keys[j] != "" and (province_keys[j] != new_keys[i] and province_keys_length != 0):
                child_tweet = ("⚠️ Coronavirus Update ⚠️\n\n"
                f"{clocks[hour]} {datecode}\n\n"
                f"🌐 COVID-19 spotted for the first time in {province_keys[j]}\n\n"
                f"☣️ {jh_parsed_data[new_keys[i]]['province_data'][province_keys[j]][0]:,} cases\n"
                f"💀 {jh_parsed_data[new_keys[i]]['province_data'][province_keys[j]][1]:,} dead\n"
                f"✅ {jh_parsed_data[new_keys[i]]['province_data'][province_keys[j]][2]:,} recovered\n\n"
                f"🗓️ Updated {jh_parsed_data[new_keys[i]]['province_data'][province_keys[j]][3]}")

                if footer != "":
                    child_tweet = (f"{child_tweet}\n\n"
                    f"{footer}")

                thread.append(child_tweet)

        verbose_tweets.append(thread)
        thread = []

    # Iterate across all updated countries
    historical_keys_length = len(historical_keys)
    for i in range(historical_keys_length):
        if (jh_parsed_data[historical_keys[i]]['total_confirmed'] == historical_data[historical_keys[i]]['total_confirmed'] and
            jh_parsed_data[historical_keys[i]]['total_dead'] == historical_data[historical_keys[i]]['total_dead'] and
            jh_parsed_data[historical_keys[i]]['total_recovered'] == historical_data[historical_keys[i]]['total_recovered']):
            continue
        master_tweet = (f"⚠️ Coronavirus Update ⚠️\n\n"
        f"{clocks[hour]} {datecode}\n\n"
        f"🌐 Update for {historical_keys[i]}\n\n")

        if jh_parsed_data[historical_keys[i]]['total_confirmed'] != historical_data[historical_keys[i]]['total_confirmed']:
            master_tweet = (f"{master_tweet}"
            f"☣️ {jh_parsed_data[historical_keys[i]]['total_confirmed']:,} cases ({jh_parsed_data[historical_keys[i]]['total_confirmed'] - historical_data[historical_keys[i]]['total_confirmed']:+,})\n")
        else:
            master_tweet = (f"{master_tweet}"
            f"☣️ {jh_parsed_data[historical_keys[i]]['total_confirmed']:,}cases \n")

        if jh_parsed_data[historical_keys[i]]['total_dead'] != historical_data[historical_keys[i]]['total_dead']:
            master_tweet = (f"{master_tweet}"
            f"💀 {jh_parsed_data[historical_keys[i]]['total_dead']:,} dead ({jh_parsed_data[historical_keys[i]]['total_dead'] - historical_data[historical_keys[i]]['total_dead']:+,})\n")
        else:
            master_tweet = (f"{master_tweet}"
            f"💀 {jh_parsed_data[historical_keys[i]]['total_dead']:,} dead\n")

        if jh_parsed_data[historical_keys[i]]['total_recovered'] != historical_data[historical_keys[i]]['total_recovered']:
            master_tweet = (f"{master_tweet}"
            f"✅ {jh_parsed_data[historical_keys[i]]['total_recovered']:,} recovered ({jh_parsed_data[historical_keys[i]]['total_recovered'] - historical_data[historical_keys[i]]['total_recovered']:+,})")
        else:
            master_tweet = (f"{master_tweet}"
            f"✅ {jh_parsed_data[historical_keys[i]]['total_recovered']:,}recovered")

        if footer != "":
            master_tweet = (f"{master_tweet}\n\n"
            f"{footer}")

        thread.append(master_tweet)

        province_keys = list(jh_parsed_data[historical_keys[i]]['province_data'].keys())
        historical_province_keys = list(historical_data[historical_keys[i]]['province_data'].keys())
        new_province_keys = list(set(province_keys) - set(historical_province_keys))

        new_province_keys_length = len(new_province_keys)

        # Iterate across all new states/provinces in updated countries
        for j in range(new_province_keys_length):
            if new_province_keys[j] != "" and (new_province_keys[j] != historical_keys[i] and new_province_keys_length != 0):
                child_tweet = (f"{datecode}\n\n"
                f"🌐 COVID-19 spotted for the first time in {new_province_keys[j]}\n\n"
                f"☣️ {jh_parsed_data[historical_keys[i]]['province_data'][new_province_keys[j]][0]:,} cases\n"
                f"💀 {jh_parsed_data[historical_keys[i]]['province_data'][new_province_keys[j]][1]:,} dead\n"
                f"✅ {jh_parsed_data[historical_keys[i]]['province_data'][new_province_keys[j]][2]:,} recovered\n\n"
                f"🗓️ Updated {jh_parsed_data[historical_keys[i]]['province_data'][new_province_keys[j]][3]}")

                if footer != "":
                    child_tweet = (f"{child_tweet}\n\n"
                    f"{footer}")

                thread.append(child_tweet)

        historical_province_keys_length = len(historical_province_keys)

        # Iterate across all updated states/provinces in updated countries
        for j in range(historical_province_keys_length):
            if (historical_province_keys[j] == "" or (historical_province_keys[j] == historical_keys[i] and historical_province_keys_length == 0)) or jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][0:3] == historical_data[historical_keys[i]]['province_data'][historical_province_keys[j]][0:3]:
                continue

            child_tweet = (f"{datecode}\n\n"
            f"🌐 Update for {historical_province_keys[j]}.\n\n")

            if jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][0] != historical_data[historical_keys[i]]['province_data'][historical_province_keys[j]][0]:
                child_tweet = (f"{child_tweet}"
                f"☣️ {jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][0]:,} cases ({jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][0] - historical_data[historical_keys[i]]['province_data'][historical_province_keys[j]][0]:+,})\n")
            else:
                child_tweet = (f"{child_tweet}"
                f"☣️ {jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][0]:,} cases\n")

            if jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][1] != historical_data[historical_keys[i]]['province_data'][historical_province_keys[j]][1]:
                child_tweet = (f"{child_tweet}"
                f"💀 {jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][1]:,} dead ({jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][1] - historical_data[historical_keys[i]]['province_data'][historical_province_keys[j]][1]:+,})\n")
            else:
                child_tweet = (f"{child_tweet}"
                f"💀 {jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][1]:,} dead\n")

            if jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][2] != historical_data[historical_keys[i]]['province_data'][historical_province_keys[j]][2]:
                child_tweet = (f"{child_tweet}"
                f"✅ {jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][2]:,} recovered ({jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][2] - historical_data[historical_keys[i]]['province_data'][historical_province_keys[j]][2]:+,})")
            else:
                child_tweet = (f"{child_tweet}"
                f"✅ {jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][2]:,} recovered")

            child_tweet = (f"{child_tweet}\n"
            f"🗓️ Updated {jh_parsed_data[historical_keys[i]]['province_data'][historical_province_keys[j]][3]}")

            if footer != "":
                child_tweet = (f"{child_tweet}\n\n"
                f"{footer}")

            thread.append(child_tweet)

        print(thread)
        verbose_tweets.append(thread)
        thread = []

    return verbose_tweets