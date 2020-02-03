#!/usr/bin/python3
import argparse
import getopt
import time
import requests, json
import gspread pickle
from oauth2client.service_account import ServiceAccountCredentials

# Import our Twitter credentials from credentials.py
from credentials import *

def get_twitter_api():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    
    return auth, api

def get_gdrive_api():
    # get API access
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    return client

def get_jh_worksheet():
    # get API access and fetch latest worksheet
    client = get_gdrive_api()
    jh_sheet = client.open_by_key('1ZJCEHKijIMVSJvH74C-LIUJb7BAHqj6b')
    jh_worksheet = jh_sheet.get_worksheet(0)

    return jh_worksheet

def get_qq(headers):
    # Get QQ
    try:
        qq_res = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5',headers=headers)
        qq_json = json.loads(qq_res.content.decode())
        qq_json_data = json.loads(qq_json['data'])
        qq_total = qq_json_data['chinaTotal']['confirm']
        qq_suspect = qq_json_data['chinaTotal']['suspect']
        qq_recovered = qq_json_data['chinaTotal']['heal']
        qq_dead = qq_json_data['chinaTotal']['dead']
    except:
        qq_total = 'NaN'
        qq_suspect = 'NaN'
        qq_recovered = 'NaN'
        qq_dead = 'NaN'

    return qq_total, qq_suspect, qq_recovered, qq_dead

def get_jh(headers):
    # Get Johns Hopkins total
    try:
        jh_total_res = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers)
        jh_total_json = json.loads(jh_total_res.content.decode())
        jh_total = jh_total_json['features'][0]['attributes']['value']
    except:
        jh_total = 'NaN'

    # Get Johns Hopkins deaths
    try:
        jh_dead_res = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Deaths%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers)
        jh_dead_json = json.loads(jh_dead_res.content.decode())
        jh_dead = jh_dead_json['features'][0]['attributes']['value']
    except:
        jh_dead = 'NaN'

    # Get Johns Hopkins recoveries
    try:
        jh_recovered_res = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Recovered%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers)
        jh_recovered_json = json.loads(jh_recovered_res.content.decode())
        jh_recovered = jh_recovered_json['features'][0]['attributes']['value']
    except:
        jh_recovered = 'NaN'

    return jh_total, jh_dead, jh_recovered, jh_worksheet

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
    f"""QQ = Tencent QQ News\n""")
    
    # Define hashtags
    hashtags = "#WuhanPneumonia #WuhanCoronavirus #coronavirus #nCov #2019nCov #nCov2019"

    # Build statistics tweet
    stats_tweet = (f"""{datecode}\n\n"""
    f"""{stats}\n"""
    f"""{hashtags}""")

    return stats_tweet

def build_replies(datecode):
    jh_worksheet = get_jh_worksheet()

    print("test string")
    print(jh_worksheet.cell(1, 1).value)
    return []

def output(send_flag, api, tweet_list):
    # Prepare for list output
    length = len(tweet_list)

    # Output master tweet
    print(f"\n{tweet_list[0]}")

    if send_flag == True:
        prev_tweet = api.update_status(tweet_list[0]

    # Output and post replies in list
    for i in range(1, length):
        # Test print / terminal output
        print(f"\n{tweet_list[i]}")

        # Send tweet
        if send_flag == True:
            time.sleep(5)
            prev_tweet = api.update_status("@" + prev_tweet.user.screen_name + "\n\n" + tweet_list[i], prev_tweet.id)

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
    auth, api = get_twitter_api()

    # Get current UTC time
    utctime = time.gmtime()
    datecode = f"{utctime.tm_year:04}-{utctime.tm_mon:02}-{utctime.tm_mday:02} {utctime.tm_hour:02}:{utctime.tm_min:02} UTC"
 
    # Create tweet list
    tweet_list = []

    # Build stats tweet and add to list
    stats_tweet = build_stats_tweet(datecode)
    tweet_list.extend([stats_tweet])

    replies[] = build_replies()

    # Send tweets
    output(not args.notweet, api, tweet_list)

if __name__ == "__main__":
    main()