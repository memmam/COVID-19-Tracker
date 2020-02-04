# 2019-nCoV Tracker v2.0-beta-3a
Twitter bot for posting information on spread of 2019-nCov. The official instance of this bot can be found at [@2019nCovTracker](https://twitter.com/2019nCovTracker).

# Changelog

## 2.0-beta-x:
- 2.0-beta-3a: Setup script now gives execute permissions (bugfix)
- 2.0-beta-3: Added new setup script to simplify deployment
- 2.0-beta-2a: Commented out print() left in as part of testing
- 2.0-beta-2: Added nCov.sh launcher to allow for Python virtual environments, added spreadsheet fetching for v2.0 location-based updates, fixed behavior on web request failure
- 2.0-beta: Major code refactor in preparation for currently not-implemented v2.0 location-based updates

## 1.5x:
- 1.5: Tweets now stored as a list for mass output (backend work for v2.0 update)

## 1.2x

- 1.2a: Tweet format overhaul
- 1.2: Tweet is now constructed entirely modularly across separate strings for the date, statistics, and hashtags

## 1.1x

- 1.1: Hashtags are now stored as a separate string from the main tweet f-string for ease of editing/modularity

## 1.0x

- 1.0b-1: Adjusted hashtags, re-added commas
- 1.0b: Changed hashtags, removed commas from numbers to make them all fit
- 1.0a: Removed double tweepy import
- 1.0: Initial version!

# To create your own instance:

1. Sign up for Twitter API access [here](https://developer.twitter.com/) and make note of your consumer key, consumer secret, access token, and access token secret. _TWITTER WILL ONLY SHOW YOU YOUR ACCESS TOKEN AND ACCESS TOKEN SECRET **ONCE,** SO DON'T LOSE THEM._ **DO NOT SHARE THESE WITH ANYONE OR THEY CAN TAKE OVER YOUR TWITTER ACCOUNT.**

2. Make a `credentials.py` file in the following format:

```
import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
```

3. Create a Google APIs & Services project [here](https://console.developers.google.com/), and add 'Google Sheets' in the API Library

4. Create a service account for the project you just created, with the permission 'Project Editor'

5. Download the JSON file for the service account, and put it in the same directory as `nCov.py`, named `credentials.json`

6. in the root directory of the bot, run the command `python3 -m venv venv` to create a virtual environment

7. Run Setup-nCoV.sh to create launcher scripts (cron can only run nCoV.py from venv using a launcher script, allows you to run script from terminal without having to activate venv)

8. Install the Requests, Tweepy, gspread, and oauth2client libraries and create a cronjob to run nCov.sh at an interval of your choosing. 

# About
Numbers marked 'JH' are from the [Johns Hopkins University CSSE tracker](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6).

Numbers marked 'QQ' are from the [Tencent QQ News tracker](https://news.qq.com/zt2020/page/feiyan.htm).

Both of those links lead to dashboards with visual maps as well as per-city statistics. The Johns Hopkins CSSE link is in English and sources information from the [WHO](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports), [CDC](https://www.cdc.gov/coronavirus/2019-ncov/index.html), [ECDC](https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases), [NHC](http://www.nhc.gov.cn/yjb/s3578/new_list.shtml) and [DXY](https://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=singlemessage&isappinstalled=0). The Tencent QQ News link is in Chinese and sources information from "national and local health committees". Both appear to be updated by hand, and thus are not 'up-to-the-minute'.

Johns Hopkins CSSE is at this time not publishing a 'suspected cases' count, unlike Tencent QQ News. As a result, there is only one number for suspected cases.

Tweets are time-and-datestamped based on time of data being fetched and posted to Twitter. Time-and-datestamp does NOT refer to when the information was last updated. For that, see the links above.

Tweets are in the following format:

```
YYYY-MM-DD HH:MM UTC

N,NNN,NNN (JH) / N,NNN,NNN (QQ) cases
N,NNN,NNN (QQ) suspected
N,NNN,NNN (JH) / N,NNN,NNN (QQ) deaths
N,NNN,NNN (JH) / N,NNN,NNN (QQ) recovered

JH = Johns Hopkins
QQ = Tencent QQ News

#WuhanPneumonia #WuhanCoronavirus #coronavirus #nCov #2019nCov #nCov2019
```

This bot will, if functioning normally, post an update once every hour. If any problems arise, please report them to @Math#7777 on Discord.

Credit to [@Yuu6883](https://github.com/Yuu6883) for helping write the web scraping code.

Credit to users on the [Weaponsandstuff93](https://www.youtube.com/channel/UCAbwEStxHetWMGvaq9FIF_w) Discord server for helping devise the post format.

Credit to Ensheng Dong ([@Energeticodefish](https://github.com/enshengdong) on Github) from the Center for Systems Science and Engineering at Johns Hopkins University for creating the Johns Hopkins 2019-nCoV tracker, and for replying to my emails about Google Sheets access.

Credit to the CDC for the official instance's Twitter profile picture.

This bot is powered by Python 3 and the [Requests](https://requests.readthedocs.io/en/master/), [Tweepy](https://www.tweepy.org/), and [gspread](https://github.com/burnash/gspread) libraries.
