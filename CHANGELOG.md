# Changelog

## 10.6:
- Changes to Setup-nCoV.sh to prevent cronjob mail spam

## 10.5x:
- 10.5a
    - Slight format fix to Setup-nCoV.sh, otherwise identical
- 10.5: CUMULATIVE UPDATE rolling up several versions of unreleased updates
    - 10.5:
        - Code is now fully commented
        - Fixed bug in tweet resending code not leading to proper exit condition
        - Fixed MAJOR bug causing inaccurate active case numbers in United States
    - 10.4:
        - Removed config file entries and unnecessary code fragments related to NumPy / PIL graph concatenation
    - 10.3:
        - No longer reliant on NumPy / PIL for graphs, code originally by JimChr - R4GN4R removed
    - 10.2:
        - Graph image now inside embed
    - 10.1-b:
        - Fixed resend-attempt code, fixed many bugs related to backend rework
    - 10.0-b:
        - MASSIVE backend rework to allow for changing output countries based on a config file instead of being hardcoded (country order changes no longer tracked in changelog)
    - 9.3-b
        - Fixed and reworked run logging (was not logging to file, was not logging manual bot execution)
        - Changed Discord output to [World, EU+UK, US, Spain, Italy, UK, Canada, South Korea, China], with graph output on both Twitter and Discord being a 3x3 composite of relevant graphs
    - 9.2-b
        - Added minor ticks to graph Y axis
    - 9.1-b
        - Number of days in graph now automatically adjusts each day from a per-graph minimum to a global maximum
        - Replaced Canada with Italy
    - 9.0-b1:
        - Fixed globe emoji displaying Europe/Africa instead of the Americas during American daytime hours
    - 9.0-b:
        - Reduced code repetition by breaking out Discord, Twitter, and graph generation into functions
        - Partially implemented new, rewritten Discord webhook (now uses inline fields in embed, 10.x non-beta release will put the image inside the embed as well)
    - 8.2-b
        - Discord webhook now outputs a composite graph of figures worldwide, in the US, in Canada, in the United Kingdom, in the EU, and in China (credit to JimChr - R4GN4R on StackOverflow for the code for this)
    - 8.1-b:
        - Added graph colors, reworked graph ticks/labels, added grid to graphs, generally cleaned up graphing code
        - Removed year from graph labels, increased graph from 'last 9 days' to 'last 12 days'
    - 8.0-b
        - Added graphs for worldwide, US, UK, and EU counts, removed code related to location-based updates, as feature is no longer on roadmap
    - 7.0-b1:
        - Replaced China with UK on Twitter output (both UK and China are retained on Discord output)
        - Removed deltas on Twitter output, changed tweet format to be even more compact to allow for a footer explaining how to read the new compact tweets
    - 7.0-b:
       - Rewrote how the bot fetches and handles JHU data, further compacted tweet, replaced 'Without China' count with US, Canada, EU, and China counts
    - 6.0-b2:
        - Compacted tweet format due to tweet length causing bot failure (code not formally 'released' as a specific build, pushed to GitHub as part of  release)

## 6.0-bx:
- 6.0-b1: Fixed Setup-nCoV.sh to use new footer format, removed Setup-nCoV.sh user input (no longer needed)
- 6.0-b: Added Discord webhook functionality, FINALLY fixed output log archiving

## 5.0-bx:
- 5.0-b: Added 'outside China' count, total rewrite of tweet format (code pushed to GitHub but not formally 'released' as a specific build)

## 4.2-beta-x:
- 4.2-b1: Major changes to Twitter-related logic to prevent bugs caused by Twitter being over-capacity.
- 4.2-beta: Added 'last updated' output to Twitter bio

## 4.1-beta-x:
- 4.1-beta: Removed Tencent, added 'active' count, fixed various bugs with data fetching (code pushed to GitHub but not formally 'released' as a specific build)

## 4.0-beta-x:
- 4.0-beta-1: Fixed setup script, stubbed out / removed Google Sheets API (verbose output currently hardcoded to produce no output pending csv update)
- 4.0-beta: Complete overhaul of front-facing UI, added full parsing engine and supporting code for location-based updates using Google Sheets (which was deprecated right as this release was being finalized, hence the beta and new version number, I need to rewrite it for GitHub-hosted .csv files)

## 3.2-beta-x
- 3.2-beta-1: CRITICAL bugfix in set-up script (cronjob called wrong file)
- 3.2-beta: Rewrote the setup procedure; aside from setting up API access and creating your `credentials.py` and `credentials.json` files, you should now only need to run the setup script for the bot to work. I also fixed Setup-nCoV.py creating `hashtags.txt` instead of `footers.txt`.

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
