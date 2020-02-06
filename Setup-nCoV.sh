#!/bin/bash

# 2019-nCoV Tracker v3.0-beta-3
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-05
#
# A Twitter bot for posting information on the spread of the 2019-nCoV outbreak
#
# Uses Requests, Tweepy, and gspread libraries
#
# File: Setup-nCoV.sh
# Purpose: Creates launcher scripts for 2019-nCoV Tracker

# launcher script function
make_launcher()
{
    echo "#!/bin/bash" > $1
    echo -n "cd " >> $1
    echo `pwd` >> $1
    echo "source ./venv/bin/activate" >> $1
    echo "python3 $2" >> $1
}

# create hashtags.txt
echo "Please retweet to spread awareness." > hashtags.txt
echo "" >> hashtags.txt
echo -n "#WuhanCoronavirus #coronavirus #nCoV #2019nCoV" >> hashtags.txt

# create nCoV.sh
make_launcher "nCoV.sh" "nCoV.py"

# create nCoV-notweet.sh
make_launcher "nCoV-notweet.sh" "nCoV.py --notweet"

# create nCoV-noload.sh
make_launcher "nCoV-noload.sh" "nCoV.py --noload"

# create nCoV-notweet-noload.sh
make_launcher "nCoV-notweet-noload.sh" "nCoV.py --notweet --noload"

# create test.sh
make_launcher "test.sh" "test_tweet.py"

# permissions
chmod a+x nCoV*.sh
chmod a+x test.sh