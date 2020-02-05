#!/usr/bin/python3

# 2019-nCoV Tracker v3.0-beta-1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-04
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
def build_stats_tweet(datecode):
    # request header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    # scrapers
    qq_total, qq_suspect, qq_recovered, qq_dead = get_qq(headers)
    jh_total, jh_dead, jh_recovered = get_jh(headers)

    # Construct statistics
    stats = (f"""{jh_total:,} (JH) / {qq_total:,} (QQ) cases\n"""
    f"""{qq_suspect:,} (QQ) suspected\n"""
    f"""{jh_dead:,} (JH) / {qq_dead:,} (QQ) deaths\n"""
    f"""{jh_recovered:,} (JH) / {qq_recovered:,} (QQ) recoveries\n\n"""
    f"""JH = Johns Hopkins\n"""
    f"""QQ = QQ News\n""")
    
    # Define hashtags
    with open ("hashtags.txt", "r") as hash_file:
        hashtags=hash_file.readline().replace('\n', '')
        hash_file.close()

    # Build statistics tweet
    stats_tweet = (f"""{datecode}\n\n"""
    f"""{stats}\n"""
    f"""Please retweet to spread awareness.\n\n"""
    f"""{hashtags}""")

    return stats_tweet

# Parser for JH spreadsheet
def parse_jh(jh_worksheet_list):
    length = len(jh_worksheet_list)
    countries_list = []
    jh_processed_data = []

    # Core parser logic

    # Iterate over sheet
    for i in range(length):
        # If a given country is already in the processed data, append the province to it
        if jh_worksheet_list[i].get('Country/Region') in countries_list:
            country_index = countries_list.index(jh_worksheet_list[i].get('Country/Region'))
            jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region')).get('province_data')[jh_worksheet_list[i].get('Province/State')] = [jh_worksheet_list[i].get('Confirmed'),  jh_worksheet_list[i].get('Deaths'),  jh_worksheet_list[i].get('Recovered'),  jh_worksheet_list[i].get('Last Update')]
            jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region'))['total_confirmed'] = jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region')).get('total_confirmed') + jh_worksheet_list[i].get('Confirmed')
            jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region'))['total_dead'] = jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region')).get('total_dead') + jh_worksheet_list[i].get('Deaths')
            jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region'))['total_recovered'] = jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region')).get('total_recovered') + jh_worksheet_list[i].get('Recovered')
        
        # Else, create a new country entry in the processed data, and populate it with the current province
        else:
            countries_list.append(jh_worksheet_list[i].get('Country/Region'))
            jh_processed_data.append({
                jh_worksheet_list[i].get('Country/Region'): {
                    'province_data': {jh_worksheet_list[i].get('Province/State'): [jh_worksheet_list[i].get('Confirmed'),  jh_worksheet_list[i].get('Deaths'),  jh_worksheet_list[i].get('Recovered'),  jh_worksheet_list[i].get('Last Update')]},
                    'total_confirmed': jh_worksheet_list[i].get('Confirmed'),
                    'total_dead': jh_worksheet_list[i].get('Deaths'),
                    'total_recovered': jh_worksheet_list[i].get('Recovered')
                }})

    jh_processed_data.insert(0, countries_list)
    
    jh_sheet_json = json.loads(json.dumps(jh_processed_data))

    return jh_sheet_json

# Get and parse Johns Hopkins CSSU data
def get_parse_jh():
    jh_worksheet = get_jh_worksheet()

    # Catch failed spreadsheet load
    if jh_worksheet == 0:
        return 0

    jh_worksheet_list = jh_worksheet.get_all_records()

    jh_sheet_json = parse_jh(jh_worksheet_list)

    return jh_sheet_json

# Build replies from processed data
def build_replies(datecode):
    jh_sheet_json = get_parse_jh()

    # Catch failed spreadsheet load
    if jh_sheet_json == 0:
        return []

    print(jh_sheet_json)

    return []