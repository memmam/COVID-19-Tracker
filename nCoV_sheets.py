#!/usr/bin/python3

# 2019-nCoV Tracker v3.0-beta-1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-04
#
# A Twitter bot for posting information on the spread of the 2019-nCoV outbreak
#
# Uses Requests, Tweepy, and gspread libraries
#
# File: nCoV_gsheets.py
# Purpose: Methods for nCoV.py that use Google Sheets API

# For parsing Johns Hopkins spreadsheet
import gspread

# For API access
from oauth2client.service_account import ServiceAccountCredentials

# Get API access
def get_sheets_api():
    # get API access
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    return client

# Get Johns Hopkins CSSU data
def get_jh_worksheet():

    # get API access and fetch latest worksheet
    client = get_sheets_api()

    # Catch failed spreadsheet load
    try:
        jh_sheet = client.open_by_key('1wQVypefm946ch4XDp37uZ-wartW4V7ILdg-qYiDXUHM')
    except:
        return 0

    jh_worksheet = jh_sheet.get_worksheet(0)

    return jh_worksheet