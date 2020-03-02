#!/bin/bash

# 2019-nCoV Tracker v4.0-beta-1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-09
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

# get user input
echo "Please enter the name of your second bot. If none, just press enter."
read botname

# create footers
if [ botname == "" ]
then
    echo "🔁 Retweet for awareness" > footer.txt
    echo "" >> footer.txt
    echo -n "#coronavirus #COVID19 #2019nCoV" >> footer.txt

    cat footer.txt > footer_verbose.txt
else
    echo "🔁 Retweet for awareness" > footer.txt
    echo "" >> footer.txt
    
    cat footer.txt > footer_verbose.txt

    echo "🔎 @$botname for details" >> footer.txt
    echo "" >> footer.txt

    echo -n "#coronavirus #COVID19 #2019nCoV" >> footer.txt
    echo -n "#coronavirus #COVID19 #2019nCoV" >> footer_verbose.txt
fi

# create nCoV.sh
make_launcher "nCoV.sh" "nCoV.py"

# create nCoV-notweet.sh
make_launcher "nCoV-notweet.sh" "nCoV.py --notweet"

# create nCoV-verbose.sh
make_launcher "nCoV-verbose.sh" "nCoV.py --verbose"

# create nCoV-notweet-verbose.sh
make_launcher "nCoV-notweet-verbose.sh" "nCoV.py --notweet --verbose"

# create virtual environment and install packages
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install pandas requests==2.22.0 tweepy==3.8.0

# create cronjobs
mkdir cron_hist

cmd="`pwd`/nCoV.sh >> `pwd`/cron_reports.txt"
job="0 */2 * * * $cmd"
( crontab -l | grep -v -F "$cmd" ; echo "$job" ) | crontab -

cmd="mv `pwd`/cron_reports.txt `pwd`/cron_hist/cron_\`date\`.txt"
job="0 0 * * * $cmd"
( crontab -l | grep -v -F "$cmd" ; echo "$job" ) | crontab -

# permissions
chmod a+x nCoV*.sh

echo $'\nTesting... If the following succeeds, the bot is set up and working! If not, you likely credentials.py or credentials.json.\n'
./nCoV-notweet-verbose.sh
