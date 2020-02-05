#!/usr/bin/python3

# 2019-nCoV Tracker v3.0-beta-1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-04
#
# A Twitter bot for posting information on the spread of the 2019-nCoV outbreak
#
# Uses Requests, Tweepy, and gspread libraries
#
# File: nCoV_parse.py
# Purpose: Methods for parsing Johns Hopkins data

# FOR TESTING - TODO: REMOVE
import pprint

# For saving and loading of historical Johns Hopkins data
import pickle

# Import nCoV-parse methods for parsing Johns Hopkins data
from nCoV_sheets import *

# Parser for JH spreadsheet
def parse_jh(jh_worksheet_list):
    length = len(jh_worksheet_list)
    countries_list = []
    jh_processed_data = []

    # Core parser logic
    for i in range(length):
        if jh_worksheet_list[i].get('Country/Region') in countries_list:
            country_index = countries_list.index(jh_worksheet_list[i].get('Country/Region'))
            jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region')).get('province_data')[jh_worksheet_list[i].get('Province/State')] = [jh_worksheet_list[i].get('Confirmed'),  jh_worksheet_list[i].get('Deaths'),  jh_worksheet_list[i].get('Recovered'),  jh_worksheet_list[i].get('Last Update')]
            jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region'))['total_confirmed'] = jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region')).get('total_confirmed') + jh_worksheet_list[i].get('Confirmed')
            jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region'))['total_dead'] = jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region')).get('total_dead') + jh_worksheet_list[i].get('Deaths')
            jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region'))['total_recovered'] = jh_processed_data[country_index].get(jh_worksheet_list[i].get('Country/Region')).get('total_recovered') + jh_worksheet_list[i].get('Recovered')
        else:
            countries_list.append(jh_worksheet_list[i].get('Country/Region'))
            jh_processed_data.append({
                jh_worksheet_list[i].get('Country/Region'): {
                    'province_data': {jh_worksheet_list[i].get('Province/State'): [jh_worksheet_list[i].get('Confirmed'),  jh_worksheet_list[i].get('Deaths'),  jh_worksheet_list[i].get('Recovered'),  jh_worksheet_list[i].get('Last Update')]},
                    'total_confirmed': jh_worksheet_list[i].get('Confirmed'),
                    'total_dead': jh_worksheet_list[i].get('Deaths'),
                    'total_recovered': jh_worksheet_list[i].get('Recovered')
                }})

    jh_processed_data.insert(0, countries_list)
    
    return jh_processed_data

# Get and parse Johns Hopkins CSSU data
def get_parse_jh():
    jh_worksheet = get_jh_worksheet()

    # Catch failed spreadsheet load
    if jh_worksheet == 0:
        return 0

    jh_worksheet_list = jh_worksheet.get_all_records()

    jh_processed_data = parse_jh(jh_worksheet_list)

    return jh_processed_data

# Build replies from processed data
def build_replies(datecode):
    jh_processed_data = get_parse_jh()

    # Catch failed spreadsheet load
    if jh_processed_data == 0:
        return []

    pp = pprint.PrettyPrinter()

    pp.pprint(jh_processed_data)

    return []