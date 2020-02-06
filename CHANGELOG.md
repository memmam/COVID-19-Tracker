# Changelog

## 3.0-beta-x
- 3.0-beta-3: Replaced `hashtags.txt` with `footer.txt`, which defines both the 'Please retweet' message as well as the hashtags. This file is now created by the installer script. Fixed a MAJOR bug in 3.0-beta-2 where the bot would post `ABOT` instead of simply not posting. Fixed a behavior where the bot would only not produce a tweet if tweeting was disabled.
- 3.0-beta-2: Added parser for Johns Hopkins spreadsheet, switched from pickle to JSON, bot will now only post if data has changed (aborts after pulling data unless using --notweet)
- 3.0-beta-1: Improved comments, added headers, rewrote test_tweet.py to use new method structure
- 3.0-beta: Split code across multiple files instead of one long one. Location-based tracking pushed to final v3.0 release (still not implemented at this time).

## 2.0-beta-x:
- 2.0-beta-4a: Fixed potential bug with hashtags.txt import
- 2.0-beta-4: Made hashtags user-editable in a `hashtags.txt`, switched all references of 'nCov' to 'nCoV'
- 2.0-beta-3a: Setup script now gives execute permissions (bugfix)
- 2.0-beta-3: Added new setup script to simplify deployment
- 2.0-beta-2a: Commented out print() left in as part of testing
- 2.0-beta-2: Added nCoV.sh launcher to allow for Python virtual environments, added spreadsheet fetching for v2.0 location-based updates, fixed behavior on web request failure
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
