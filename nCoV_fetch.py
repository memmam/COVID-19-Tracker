#!/usr/bin/python3

# Coronavirus Disease Tracker v10.7a
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-04-14
#
# A Twitter/Discord bot for posting information on the spread of the COVID-19
# outbreak
#
# Uses Requests, Tweepy, pandas, discord-webhook, and matplotlib libraries
#
# File: nCoV_fetch.py
# Purpose: Methods for nCoV.py involving HTTP requests

# For Johns Hopkins web requests
from requests import get

# To process requested data
from json import loads

# Import Counter for summing EU dicts
from collections import Counter

# Fetch Johns Hopkins CSSE data
def get_jh():
    header = {'User-Agent': \
             ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
             'like Gecko) Chrome/56.0.2924.76 Safari/537.36'), \
             "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": \
             "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
             ,"Accept-Language": "en-US,en;q=0.5","Accept-Encoding": \
             "gzip, deflate"}

    # Get Johns Hopkins total
    for attempt_no in range(1,3):
        try:
            jh_total_res = get \
                (('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/se'
                  'rvices/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&r'
                  'eturnGeometry=false&spatialRel=esriSpatialRelIntersects&outF'
                  'ields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22'
                  '%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisti'
                  'cFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint'
                  '=true'),headers=header, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins deaths
    for attempt_no in range(1,3):
        try:
            jh_dead_res = get \
                (('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/se'
                  'rvices/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&r'
                  'eturnGeometry=false&spatialRel=esriSpatialRelIntersects&outF'
                  'ields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22'
                  '%2C%22onStatisticField%22%3A%22Deaths%22%2C%22outStatisticFi'
                  'eldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint' \
                  '=true'),headers=header, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins recoveries
    for attempt_no in range(1,3):
        try:
            jh_recovered_res = get \
                (('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/se'
                  'rvices/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&r'
                  'eturnGeometry=false&spatialRel=esriSpatialRelIntersects&outF'
                  'ields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22'
                  '%2C%22onStatisticField%22%3A%22Recovered%22%2C%22outStatisti'
                  'cFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint'
                  '=true'),headers=header, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins totals per-country
    for attempt_no in range(1,3):
        try:
            jh_countries_res = get \
                (('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/se'
                  'rvices/ncov_cases/FeatureServer/2/query?f=json&where=1%3D1&r'
                  'eturnGeometry=false&spatialRel=esriSpatialRelIntersects&outF'
                  'ields=*&orderByFields=Confirmed%20desc&resultOffset=0&result'
                  'RecordCount=190&cacheHint=true'),headers=header, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins total time series CSV
    for attempt_no in range(1,3):
        try:
            jh_total_csv_res = get \
                (('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/ma'
                  'ster/csse_covid_19_data/csse_covid_19_time_series/time_serie'
                  's_covid19_confirmed_global.csv'),headers=header, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins deaths time series CSV
    for attempt_no in range(1,3):
        try:
            jh_dead_csv_res = get \
                (('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/ma'
                  'ster/csse_covid_19_data/csse_covid_19_time_series/time_serie'
                  's_covid19_deaths_global.csv'),headers=header, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins recoveries time series CSV
    for attempt_no in range(1,3):
        try:
            jh_recovered_csv_res = get \
                (('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/ma'
                  'ster/csse_covid_19_data/csse_covid_19_time_series/time_serie'
                  's_covid19_recovered_global.csv'),headers=header, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Load Johns Hopkins world totals as JSON
    jh_total_json = loads(jh_total_res.content.decode())
    jh_dead_json = loads(jh_dead_res.content.decode())
    jh_recovered_json = loads(jh_recovered_res.content.decode())

    # Load Johns Hopkins totals per-country as JSON
    jh_countries_json = loads(jh_countries_res.content.decode())
    jh_countries = jh_countries_json['features']

    countries_length = len(jh_countries)
    jh_countries_format = {}

    # Create dictionary of dictionaries listing per-country totals
    for i in range(countries_length):
        jh_countries_format[jh_countries[i]['attributes']['Country_Region']] = \
            {'Confirmed': jh_countries[i]['attributes']['Confirmed'],
            'Deaths': jh_countries[i]['attributes']['Deaths'],
            'Recovered': jh_countries[i]['attributes']['Recovered']}

    # Create 'World' and 'EU' entries in data
    # 'World' uses already-summed totals from other data
    # 'EU' sums member country totals
    jh_countries_format['World'] = {'Confirmed': jh_total_json['features'][0] \
        ['attributes']['value'], 'Deaths': jh_dead_json['features'][0] \
        ['attributes']['value'],'Recovered': jh_recovered_json['features'][0] \
        ['attributes']['value']}
    jh_countries_format['EU'] = Counter(jh_countries_format['Austria']) + \
            Counter(jh_countries_format['Belgium']) + \
            Counter(jh_countries_format['Bulgaria']) + \
            Counter(jh_countries_format['Croatia']) + \
            Counter(jh_countries_format['Cyprus']) + \
            Counter(jh_countries_format['Czechia']) + \
            Counter(jh_countries_format['Denmark']) + \
            Counter(jh_countries_format['Estonia']) + \
            Counter(jh_countries_format['Finland']) + \
            Counter(jh_countries_format['France']) + \
            Counter(jh_countries_format['Germany']) + \
            Counter(jh_countries_format['Greece']) + \
            Counter(jh_countries_format['Hungary']) + \
            Counter(jh_countries_format['Ireland']) + \
            Counter(jh_countries_format['Italy']) + \
            Counter(jh_countries_format['Latvia']) + \
            Counter(jh_countries_format['Lithuania']) + \
            Counter(jh_countries_format['Luxembourg']) + \
            Counter(jh_countries_format['Malta']) + \
            Counter(jh_countries_format['Netherlands']) + \
            Counter(jh_countries_format['Poland']) + \
            Counter(jh_countries_format['Portugal']) + \
            Counter(jh_countries_format['Romania']) + \
            Counter(jh_countries_format['Slovakia']) + \
            Counter(jh_countries_format['Slovenia']) + \
            Counter(jh_countries_format['Spain']) + \
            Counter(jh_countries_format['Sweden']) + \
            Counter(jh_countries_format['United Kingdom'])

    # Create a dictionary of time series CSV data, for use in nCoV_csv.py
    jh_csv_dict = {'Confirmed': jh_total_csv_res.content,
        'Deaths': jh_dead_csv_res.content,
        'Recovered': jh_recovered_csv_res.content}

    return jh_countries_format, jh_csv_dict
