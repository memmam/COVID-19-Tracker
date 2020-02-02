import time
import requests
import json

# Import our Twitter credentials from credentials.py
from credentials import *

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

# request header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

# Get current UTC time
utctime = time.gmtime()

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

# Build tweet string
nCov_tweet = f"""{utctime.tm_year:04}-{utctime.tm_mon:02}-{utctime.tm_mday:02} {utctime.tm_hour:02}:{utctime.tm_min:02}:{utctime.tm_sec:02} UTC

{jh_total:,} (JH) / {qq_total:,} (QQ) confirmed cases
{qq_suspect:,} (QQ) suspected cases
{jh_dead:,} (JH) / {qq_dead:,} (QQ) confirmed deaths
{jh_recovered:,} (JH) / {qq_recovered:,} (QQ) confirmed recoveries

JH = Johns Hopkins, QQ = Tencent QQ News

#2019nCov #coronavirus"""

# Test print / terminal output
print(nCov_tweet)

# Send tweet
api.update_status(nCov_tweet)
