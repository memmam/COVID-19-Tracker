# COVID-19 Tracker v4.2-beta
Twitter bot for posting information on spread of Coronavirus Disease 2019 (COVID-19). The official instance of this bot can be found at [@COVID19Tracker](https://twitter.com/COVID19Tracker).

# NOTICES

In process of switching all references to '2019-nCoV' to 'COVID-19'.

Please note the Tencent QQ News scraping has been removed in favor of an 'active cases' count.  

The Google Sheets access for Johns Hopkins' data has been REMOVED. The `gspread` and `oauth2client` libraries (and `credentials.json` requirement) are no longer needed, and verbose output has been stubbed for the time being. This has been done in favor of Johns Hopkins' new data posting method, a collection of `.csv` files stored on [this](https://github.com/CSSEGISandData/COVID-19) GitHub repo.

# To create your own instance:

1. Sign up for Twitter API access [here](https://developer.twitter.com/) and make note of your consumer key, consumer secret, access token, and access token secret. _TWITTER WILL ONLY SHOW YOU YOUR ACCESS TOKEN AND ACCESS TOKEN SECRET **ONCE,** SO DON'T LOSE THEM._ **DO NOT SHARE THESE WITH ANYONE OR THEY CAN TAKE OVER YOUR TWITTER ACCOUNT.** If you are using a second account for verbose output, do the same with that account as well.

2. Make a `credentials.py` file in the following format:

```
import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
```

If you are using a second account for verbose output, add lines in the following format:

```
consumer_key_verbose = ''
consumer_secret_verbose = ''
access_token_verbose = ''
access_token_secret_verbose = ''
```

3. Run `Setup-nCoV.sh`. It will prompt you for the name of your second account for verbose output. If you are only using one account, just press enter. This will create your Python 3 virtual environment, install all required packages, create the launcher scripts to run the program without having to activate the virtual environment, create `footer.txt` and `footer_verbose.txt` (which contains the text and hashtags at the bottom of every tweet) with default values, create the cron job for the bot to run automatically, and test the script for you in notweet mode.

Please note the bot will automatically overwrite your Twitter bio with a 'last updated' statistic. If you have a bio you want to use in addition to this, please create 'bio_top.txt' and 'bio_bottom.txt' files containing your desired information. The last updated count will appear between the text contained in these two files, both of which are optional.

You're done! The bot should now be working.

# About
Cases, dead, and recovered counts are from the [Johns Hopkins University CSSE tracker](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6).'

This link leads to dashboards with visual maps as well as per-state statistics, in English, and sources information from the [WHO](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports), [CDC](https://www.cdc.gov/coronavirus/2019-ncov/index.html), [ECDC](https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases), [NHC](http://www.nhc.gov.cn/yjb/s3578/new_list.shtml) and [DXY](https://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=singlemessage&isappinstalled=0). It appears to be updated by hand, and thus are not 'up-to-the-minute'.

Active cases count is derived by the following formula: (cases - dead - recovered = active)

Tweets are time-and-datestamped based on time of data being fetched and posted to Twitter. Time-and-datestamp does NOT refer to when the information was last updated. For that, see the links above.

Tweets are in the following format:

```
⚠️ Coronavirus Update ⚠️

🕕 YYYY-MM-DD HH:MM UTC

☣️ NN,NNN,NNN cases (+NN,NNN)
🏥 NN,NNN,NNN active (+NN,NNN)
💀 NN,NNN,NNN dead (+NN,NNN)
✅ NN,NNN,NNN recovered (+NN,NNN)

🔁 Retweet for awareness

#coronavirus #COVID19 #2019nCoV
```

If you are using a second account for verbose data, between the last two lines is the line `🔎 @{second_bot} for details`

Verbose tweets are in the following formats:

```
⚠️ Coronavirus Update ⚠️

🕕 YYYY-MM-DD HH:MM UTC

🌐 2019-nCoV spotted for the first time in 1234567890123456789012345678

☣️ NN,NNN,NNN cases
💀 NN,NNN,NNN dead
✅ NN,NNN,NNN recovered

🗓️ Updated 2/7/20 16:33

🔁 Retweet for awareness

#coronavirus #COVID19 #2019nCoV
```

```
⚠️ Coronavirus Update ⚠️

🕕 YYYY-MM-DD HH:MM UTC

🌐 Update for 1234567890123456789012345678

☣️ NN,NNN,NNN cases (+N,NNN)
💀 NN,NNN,NNN dead (+N,NNN)
✅ NN,NNN,NNN recovered (+N,NNN)

🗓️ Updated 2/7/20 16:33

🔁 Retweet for awareness

#coronavirus #COVID19 #2019nCoV
```

This bot will, if functioning normally, check for new data once every two hours, and only post when there is new data. If any problems arise, please report them to @Math#7777 on Discord.

# Credits

Credit to [@Yuu6883](https://github.com/Yuu6883) for helping write the web scraping code.

Credit to users on the [Weaponsandstuff93](https://www.youtube.com/channel/UCAbwEStxHetWMGvaq9FIF_w) Discord server for helping devise the post format.

Credit to Ensheng Dong ([@Energeticodefish](https://github.com/enshengdong) on Github) from the Center for Systems Science and Engineering at Johns Hopkins University for replying to my emails about Google Sheets access.

Credit to the CDC for the official instance's Twitter profile picture.

This bot is powered by Python 3 and the [Requests](https://requests.readthedocs.io/en/master/), [Tweepy](https://www.tweepy.org/), and [gspread](https://github.com/burnash/gspread) libraries.

Data tracked by this bot is Copyright 2020 Johns Hopkins University.

# Terms of Use

The Johns Hopkins University data tracked by this bot is provided to the public strictly for educational and academic research purposes. The data is built from publicly available data from multiple sources, that do not always agree. Both I and Johns Hopkins University hereby disclaim any and all representations and warranties with respect to the bot and related data, including accuracy, fitness for use, and merchantability. Reliance on the bot or data for medical guidance or use of the data in commerce is strictly prohibited by both me and Johns Hopkins University.