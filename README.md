# COVID-19 Tracker v10.6
Bot for posting information on spread of Coronavirus Disease 2019 (COVID-19) to Twitter and Discord. The official instance of this bot can be found at [@COVID19Tracker](https://twitter.com/COVID19Tracker).

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

3. Run `Setup-nCoV.sh`. This will create your Python 3 virtual environment, install all required packages, create the launcher scripts to run the program without having to activate the virtual environment, create the cron job for the bot to run automatically, and test the script for you in notweet mode.

4. Create your `config.txt` file, using config_example.txt as a base. The config file requires 9 entries to function correctly, in the following format:

```
[FLAG EMOJI]
[DICTIONARY KEY FOR DESIRED COUNTRY]
[OUTPUT NAME FOR COUNTRY]
[MAXIMUM NUMBER OF DAYS TO CLIP OFF OF GRAPH]
[FILTER LIST] (comma-separated keylist if a 'country' is made up of multiple countries - NOT FOR 'World')
0
0
0
```

I advise you put the `World` key in there somewhere, for obvious reasons.

5. This bot can also post to Discord. In your Discord server settings, generate webhooks for whatever channels you want the bot to post in, and place each webhook URL on its own line in a `webhooks.txt` file.

Please note the bot will automatically overwrite your Twitter bio with a 'last updated' statistic. If you have a bio you want to use in addition to this, please create 'bio_top.txt' and 'bio_bottom.txt' files containing your desired information. The last updated count will appear between the text contained in these two files, both of which are optional.

You're done! The bot should now be working.

# About
Cases, dead, and recovered counts are from the [Johns Hopkins University CSSE tracker](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6).'

This link leads to dashboards with visual maps as well as per-state statistics, in English, and sources information from the [WHO](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports), [CDC](https://www.cdc.gov/coronavirus/2019-ncov/index.html), [ECDC](https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases), [NHC](http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml), [DXY](https://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=singlemessage&isappinstalled=0), [1Point3Acres](https://coronavirus.1point3acres.com/), [worldometers.info](https://www.worldometers.info/coronavirus/), [BNO News](https://bnonews.com/index.php/2020/04/the-latest-coronavirus-cases/), and [The COVID Tracking Project](https://covidtracking.com/data). It appears to be updated by hand, and thus are not 'up-to-the-minute'.

Active cases count is derived by the following formula: (cases - dead - recovered = active)

Updates are time-and-datestamped based on time of data being fetched and posted. Time-and-datestamp does NOT refer to when the information was last updated. For that, see the links above.

Tweets are in the following format:

```
🕓MM/DD ##H #COVIDXX #Coronavirus

🏳️😷X,XXX,XXX 🏥X,XXX,XXX 💀XXX,XXX 👍XXX,XXX
🏳️😷XXX,XXX 🏥XXX,XXX 💀XX,XXX 👍XXX,XXX
🏳️😷XXX,XXX 🏥XXX,XXX 💀XX,XXX 👍XXX,XXX
🏳️😷XXX,XXX 🏥XXX,XXX 💀XX,XXX 👍XXX,XXX
🏳️😷XXX,XXX 🏥XXX,XXX 💀XX,XXX 👍XXX,XXX

😷Total 🏥Active 💀Dead 👍Recovered

[IMAGE OF TIME-SERIES GRAPHS]
```

This bot also optionally can output to Discord in the form of embeds in webhook messages. Discord embeds are in the following format:

```
⚠️   Coronavirus Update   ⚠️

🏳️ [COUNTRY NAME]:	🏳️ [COUNTRY NAME]:	🏳️ [COUNTRY NAME]:			
😷 X,XXX,XXX (+XX,XXX)	😷 X,XXX,XXX (+XX,XXX)	😷 X,XXX,XXX (+XX,XXX)	
🏥 X,XXX,XXX (+XX,XXX)	🏥 X,XXX,XXX (+XX,XXX)	🏥 X,XXX,XXX (+XX,XXX)	
💀 XXX,XXX (+XX,XXX)	💀 XXX,XXX (+XX,XXX)	💀 XXX,XXX (+XX,XXX)		
👍 XXX,XXX (+XX,XXX)	👍 XXX,XXX (+XX,XXX)	👍 XXX,XXX (+XX,XXX)		

🏳️ [COUNTRY NAME]:	🏳️ [COUNTRY NAME]:	🏳️ [COUNTRY NAME]:			
😷 X,XXX,XXX (+XX,XXX)	😷 X,XXX,XXX (+XX,XXX)	😷 X,XXX,XXX (+XX,XXX)	
🏥 X,XXX,XXX (+XX,XXX)	🏥 X,XXX,XXX (+XX,XXX)	🏥 X,XXX,XXX (+XX,XXX)	
💀 XXX,XXX (+XX,XXX)	💀 XXX,XXX (+XX,XXX)	💀 XXX,XXX (+XX,XXX)		
👍 XXX,XXX (+XX,XXX)	👍 XXX,XXX (+XX,XXX)	👍 XXX,XXX (+XX,XXX)		

🏳️ [COUNTRY NAME]:	🏳️ [COUNTRY NAME]:	🏳️ [COUNTRY NAME]:			
😷 X,XXX,XXX (+XX,XXX)	😷 X,XXX,XXX (+XX,XXX)	😷 X,XXX,XXX (+XX,XXX)	
🏥 X,XXX,XXX (+XX,XXX)	🏥 X,XXX,XXX (+XX,XXX)	🏥 X,XXX,XXX (+XX,XXX)	
💀 XXX,XXX (+XX,XXX)	💀 XXX,XXX (+XX,XXX)	💀 XXX,XXX (+XX,XXX)		
👍 XXX,XXX (+XX,XXX)	👍 XXX,XXX (+XX,XXX)	👍 XXX,XXX (+XX,XXX)		

[IMAGE OF TIME-SERIES GRAPHS]

😷Total 🏥Active 💀Dead 👍Recovered

🕓 Last Updated: YYYY-MM-DD HH:MM UTC
```

In both cases, updates will contain graphs showing up to the last approximately 11 weeks of confirmed cases, active cases, deaths, and recoveries in your chosen countries, with a monimum bound of days set by your config file.

This bot will, if functioning normally, check for new data once every two hours, and only post when there is new data. If any problems arise, please report them to @Math#7777 on Discord.

# Credits

Credit to [@Yuu6883](https://github.com/Yuu6883) for helping write the web scraping code.

Credit to users on the [Weaponsandstuff93](https://www.youtube.com/channel/UCAbwEStxHetWMGvaq9FIF_w) Discord server for helping devise the post format in early versions of the bot.

Credit to Ensheng "Frank" Dong ([@Energeticodefish](https://github.com/enshengdong) on Github) from the Center for Systems Science and Engineering at Johns Hopkins University for replying to my numerous emails concerning the JHU CSSE tracker.

Credit to the CDC for the official instance's Twitter profile picture.

This bot is powered by Python 3 and the [Requests](https://requests.readthedocs.io/en/master/), [Tweepy](https://www.tweepy.org/), [pandas](https://pandas.pydata.org/), [discord-webhook](https://github.com/lovvskillz/python-discord-webhook), and [matplotlib](https://matplotlib.org/) libraries.

Data tracked by this bot is Copyright 2020 Johns Hopkins University.

# Terms of Use

The Johns Hopkins University data tracked by this bot is provided to the public strictly for educational and academic research purposes. The data is built from publicly available data from multiple sources, that do not always agree. Both I and Johns Hopkins University hereby disclaim any and all representations and warranties with respect to the bot and related data, including accuracy, fitness for use, and merchantability. Reliance on the bot or data for medical guidance or use of the data in commerce is strictly prohibited by both me and Johns Hopkins University.
