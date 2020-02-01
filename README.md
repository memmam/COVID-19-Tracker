# 2019-nCov-Tracker
Twitter bot for posting information on spread of 2019-nCov.

# To create your own instance:

1. Make a `credentials.py` file in the following format:

```
import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
```

2. Install the Tweepy module, and create a Cron job to run nCov.py at an interval of your choosing.

# About
Numbers marked 'JH' are from the Johns Hopkins University CSSE tracker: https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6

Numbers marked 'QQ' are from the Tencent QQ News tracker: https://news.qq.com/zt2020/page/feiyan.htm

Both of those links lead to dashboards with visual maps as well as per-city statistics. The Johns Hopkins CSSE link is in English and sources information from the WHO, CDC, ECDC, NHC and DXY. The Tencent QQ News link is in Chinese and sources information from "national and local health committees".

Johns Hopkins CSSE is at this time not publishing a 'suspected cases' count, unlike Tencent QQ News. As a result, there is only one number for suspected cases.

Tweets are time-and-datestamped based on time of data being fetched and posted to Twitter. Time-and-datestamp does NOT refer to when the information was last updated. For that, see the links above.

Tweets are in the following format:

```
YYYY-MM-DD HH:MM:SS UTC

NUM (JH) / NUM (QQ) confirmed cases
NUM (QQ) suspected cases
NUM (JH) / NUM (QQ) confirmed deaths
NUM (JH) / NUM (QQ) confirmed recoveries

JH = Johns Hopkins, QQ = Tencent QQ News

#2019nCov #coronavirus
```

This bot will, if functioning normally, post an update once every hour. If any problems arise, please report them to Math#7777 on Discord.

Credit to Yuu6883 on GitHub for helping write the web scraping code.
Credit to users on the Weaponsandstuff93 Discord server for helping devise the post format.
Credit to the CDC for this account's profile picture.

This bot is powered by Python 3 and the Tweepy library.
