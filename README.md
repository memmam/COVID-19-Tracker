# 2019-nCov Tracker v1.1
Twitter bot for posting information on spread of 2019-nCov. The official instance of this bot can be found at [@2019nCovTracker](https://twitter.com/2019nCovTracker).

# Changelog

## 1.2

- 1.2: Tweet is now constructed entirely modularly across separate strings for the date, statistics, and hashtags

## 1.1

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

3. Install the Tweepy module, and create a Cron job to run nCov.py at an interval of your choosing.

# About
Numbers marked 'JH' are from the [Johns Hopkins University CSSE tracker](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6).

Numbers marked 'QQ' are from the [Tencent QQ News tracker](https://news.qq.com/zt2020/page/feiyan.htm).

Both of those links lead to dashboards with visual maps as well as per-city statistics. The Johns Hopkins CSSE link is in English and sources information from the [WHO](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports), [CDC](https://www.cdc.gov/coronavirus/2019-ncov/index.html), [ECDC](https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases), [NHC](http://www.nhc.gov.cn/yjb/s3578/new_list.shtml) and [DXY](https://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=singlemessage&isappinstalled=0). The Tencent QQ News link is in Chinese and sources information from "national and local health committees". Both appear to be updated by hand, and thus are not 'up-to-the-minute'.

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

#Wuhan #WuhanVirus #WuhanPneumonia #WuhanCoronavirus #coronavirus
```

This bot will, if functioning normally, post an update once every hour. If any problems arise, please report them to @Math#7777 on Discord.

Credit to [@Yuu6883](https://github.com/Yuu6883) for helping write the web scraping code.
Credit to users on the [Weaponsandstuff93](https://www.youtube.com/channel/UCAbwEStxHetWMGvaq9FIF_w) Discord server for helping devise the post format.
Credit to the CDC for the official instance's Twitter profile picture.

This bot is powered by Python 3 and the [Tweepy](https://www.tweepy.org/) library.
