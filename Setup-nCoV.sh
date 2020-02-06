#!/bin/bash

# 2019-nCoV Tracker v3.2-beta-1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-06
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
echo "Please retweet to spread awareness." > footer.txt
echo "" >> footer.txt
echo -n "#WuhanCoronavirus #coronavirus #nCoV #2019nCoV" >> footer.txt

# create nCoV.sh
make_launcher "nCoV.sh" "nCoV.py"

# create nCoV-notweet.sh
make_launcher "nCoV-notweet.sh" "nCoV.py --notweet"

# create nCoV-noload.sh
make_launcher "nCoV-noload.sh" "nCoV.py --noload"

# create nCoV-notweet-noload.sh
make_launcher "nCoV-notweet-noload.sh" "nCoV.py --notweet --noload"

# create virtual environment and install packages
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install requests==2.22.0 tweepy==3.8.0 gspread==3.2.0 oauth2client==4.1.3

# create cronjob
cmd="`pwd`/nCoV.sh >> cron_reports.txt"
job="0 */2 * * * $cmd"
( crontab -l | grep -v -F "$cmd" ; echo "$job" ) | crontab -

# permissions
chmod a+x nCoV*.sh

echo $'\nTesting... If the following succeeds, the bot is set up and working! If not, you likely credentials.py or credentials.json.\n'
./nCoV-notweet.sh