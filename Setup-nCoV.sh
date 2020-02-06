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

# create hashtags.txt

echo 'Please retweet to spread awareness.' > hashtags.txt
echo '' >> hashtags.txt
echo -n '#WuhanCoronavirus #coronavirus #nCoV #2019nCoV' >> hashtags.txt

# create nCoV.sh
echo '#!/bin/bash' > nCoV.sh
echo -n 'cd ' >> nCoV.sh
echo `pwd` >> nCoV.sh
echo 'source ./venv/bin/activate' >> nCoV.sh
echo 'python3 nCoV.py' >> nCoV.sh

# create nCoV.sh
echo '#!/bin/bash' > nCoV-notweet.sh
echo -n 'cd ' >> nCoV-notweet.sh
echo `pwd` >> nCoV-notweet.sh
echo 'source ./venv/bin/activate' >> nCoV-notweet.sh
echo 'python3 nCoV.py --notweet' >> nCoV-notweet.sh

# create nCoV.sh
echo '#!/bin/bash' > nCoV-noload.sh
echo -n 'cd ' >> nCoV-noload.sh
echo `pwd` >> nCoV-noload.sh
echo 'source ./venv/bin/activate' >> nCoV-noload.sh
echo 'python3 nCoV.py --noload' >> nCoV-noload.sh

# create nCoV.sh
echo '#!/bin/bash' > nCoV-notweet-noload.sh
echo -n 'cd ' >> nCoV-notweet-noload.sh
echo `pwd` >> nCoV-notweet-noload.sh
echo 'source ./venv/bin/activate' >> nCoV-notweet-noload.sh
echo 'python3 nCoV.py --notweet --noload' >> nCoV-notweet-noload.sh

chmod a+x nCoV*.sh