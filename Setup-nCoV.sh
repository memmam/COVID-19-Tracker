#!/bin/bash

# Coronavirus Disease Tracker v10.7
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-04-13
#
# A Twitter/Discord bot for posting information on the spread of the COVID-19
# outbreak
#
# Uses Requests, Tweepy, pandas, discord-webhook, and matplotlib libraries
#
# File: Setup-nCoV.sh
# Purpose: Creates launcher scripts for Coronavirus Disease Tracker

# launcher script maker function
make_launcher()
{
    echo "#!/bin/bash" > $1
    echo -n "cd " >> $1
    echo `pwd` >> $1
    echo "source ./venv/bin/activate" >> $1
    echo "date 2>&1 | tee -a run_reports.txt" >> $1
    echo "(time python3 $2) 2>&1 | tee -a run_reports.txt" >> $1
    echo "echo \"\" >> run_reports.txt 2>&1" >> $1
}

# create nCoV.sh
make_launcher "nCoV.sh" "nCoV.py"

# create nCoV-notweet.sh
make_launcher "nCoV-notweet.sh" "nCoV.py --notweet"

# create virtual environment and install packages
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install pandas==1.0.1 requests==2.22.0 tweepy==3.8.0 \
discord-webhook==0.7.1 matplotlib==3.2.1

# make directory for storing run report history
mkdir run_hist

# create cronjobs
# cronjob for running the bot
cmd="`pwd`/nCoV.sh > /dev/null 2>&1"
job="0 */2 * * * $cmd"
( crontab -l | grep -v -F "$cmd" ; echo "$job" ) | crontab -

# cronjob for storing historical data
cmd="mv `pwd`/run_reports.txt \"`pwd`/run_hist/\`date +\%F\`.txt\""
job="0 0 * * * $cmd"
( crontab -l | grep -v -F "$cmd" ; echo "$job" ) | crontab -

# permissions
chmod a+x nCoV*.sh

# test if working
echo $'\nTesting... If the following succeeds, the bot is set up and working!'
echo $'If not, you likely are missing credentials.py.'
./nCoV-notweet.sh
