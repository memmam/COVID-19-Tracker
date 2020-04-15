#!/usr/bin/python3

# Coronavirus Disease Tracker v10.7b
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-04-15
#
# A Twitter/Discord bot for posting information on the spread of the COVID-19
# outbreak
#
# Uses Requests, Tweepy, pandas, discord-webhook, and matplotlib libraries
#
# File: nCoV_twitter.py
# Purpose: Methods for nCoV.py that use Twitter and Discord APIs

# Import our Twitter credentials and Tweepy library from credentials.py
from credentials import *

# For generating timestamps and delay when resending
import time
import random

# Import Discord webhook support
from discord_webhook import DiscordWebhook, DiscordEmbed

# Get Twitter API access
def get_twitter_api(key, secret, token, token_secret):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(token, token_secret)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    
    return api

# Send nCoV tweets
def output(
    send_flag, api, tweet, stats_discord, date_discord, tweet_data, datecode, \
    hour, update_arr):

    # Logger output: tweet
    print(f"Tweet:\n{tweet}\n")

    # Send tweet
    if send_flag == True:
        # If an exception is thrown, try a total of three times; if it fails
        # all three times, raise excewption
        for attempt_no in range(0,4):
            try:
                # Add graphs to tweet
                filename = 'graph.png'
                media_ids = []
                res = api.media_upload(filename)
                media_ids.append(res.media_id)

                # Actually send tweet
                tweet_obj = api.update_status(status=tweet, \
                            media_ids=media_ids, tweet_mode='extended')

                # Write updated config file
                with open ("config.txt", "w") as tweet_file:
                    tweet_file.write("\n".join(map(str, update_arr)))
                    tweet_file.close()
                break
            except:
                if attempt_no < 3:
                    print("Retrying")
                    time.sleep(random.randint(15,30))
                else:
                    raise error
        
        # Update time last checked per Twitter profile
        lastcheckedupdate(tweet[0], send_flag, api, datecode)

    # Send Discord embeds, if webhooks file exists
    # Otherwise, skip Discord output
    with open ("webhooks.txt", "r") as webhook_file:
        webhook_urls = webhook_file.readlines()
        webhook_file.close()

        # Emoji translation key at bottom of embed
        emojikey = "😷Total 🏥Active 💀Dead 👍Recovered"

        # Create embed and populate it with case data
        embed = DiscordEmbed(color=16737792)
        for key in stats_discord:
            embed.add_embed_field(
                name=key, value=stats_discord[key], inline=True)
        embed.set_footer(text=f"{emojikey}\n{date_discord}")

        # If tweet was sent and embeds are being sent, attach image from it
        if send_flag == True:
            image_url = tweet_obj.entities['media'][0]['media_url']
            try:
                embed.set_image(url=f"{image_url}?format=png&name=4096x4096")
            except:
                pass

        # Attach tweet to embed name
        #
        # If no tweet was sent but script somehow proceeded (shouldn't be
        # possible), attach twitter account to embed name instead
        try:
            embed.set_author(
                name='⚠️ Coronavirus Update ⚠️', url=(f"https://twitter.com/"
                    f"{tweet_obj.user.screen_name}/status/"
                    f"{tweet_obj.id}"))
        except:
            embed.set_author(
                name='⚠️ Coronavirus Update ⚠️', url=(f"https://twitter.com/"
                f"{api.me().screen_name}"))

        # Scrub newlines from webhook URLs
        for i in range(len(webhook_urls)):
            webhook_urls[i] = webhook_urls[i].replace("\n", "")

        # Create webhook with given username and avatar, and add embed to it
        webhook = DiscordWebhook(url=webhook_urls, username=('Coronavirus '
            'Disease Tracker'), avatar_url=('https://pbs.twimg.com/'
            'profile_images/1223447558615265282/bACVLEWU_400x400.jpg'))
        webhook.add_embed(embed)

        # Send embed
        if send_flag == True:
            response = webhook.execute()

        # Logger output: Discord embed
        webhook_output = f"⚠️   Coronavirus Update   ⚠️\n\n"
        for key in stats_discord:
            webhook_output = f"{webhook_output}{key}\n{stats_discord[key]}\n\n"
        webhook_output = f"{webhook_output}{emojikey}\n\n{date_discord}"
        print(f"Discord webhook:\n{webhook_output}")

# Update Twitter bio with when last checked for case updates
def lastcheckedupdate(clock, send_flag, api, datecode):
    lastupdated = f"{clock} Updated {datecode}"

    # Define top of profile based on file
    try:
        with open ("bio_top.txt", "r") as top_file:
            bio_top=top_file.read()
            top_file.close()
    except:
        bio_top=""

    # Define bottom of profile based on file
    try:
        with open ("bio_bottom.txt", "r") as bottom_file:
            bio_bottom=bottom_file.read()
            bottom_file.close()
    except:
        bio_bottom=""

    # Create bio from top, last updated string, and bottom
    if bio_top != "":
        bio = (f"{bio_top}\n"
        f"{lastupdated}") 
    if bio_bottom != "":
        bio = (f"{bio}\n"
        f"{bio_bottom}")

    # If tweet was sent, update bio saying when last updated
    # Retry three times, if fail, raise error
    if send_flag == True:
        for attempt_no in range(0,4):
            try:
                api.update_profile(description=bio)
            except:
                if attempt_no < 3:
                    print("Retrying")
                    time.sleep(random.randint(15,30))
                else:
                    raise error

    # Logger output: Last updated timestamp
    print(bio)
