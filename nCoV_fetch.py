#!/usr/bin/python3

# Coronavirus Disease Tracker v6.0-b
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-03-22
#
# A Twitter bot for posting information on the spread of the COVID-19 outbreak
#
# Uses Requests, Tweepy, and pandas libraries
#
# File: nCoV_fetch.py
# Purpose: Methods for nCoV.py that use Requests

# For Johns Hopkins, Tencent QQ News data
import requests

# To process requested data
import json

# Fetch Johns Hopkins CSSE data
def get_jh(headers):
    # Get Johns Hopkins total
    for attempt_no in range(1,3):
        try:
            jh_total_res = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins deaths
    for attempt_no in range(1,3):
        try:
            jh_dead_res = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Deaths%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins recoveries
    for attempt_no in range(1,3):
        try:
            jh_recovered_res = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Recovered%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins total for China
    for attempt_no in range(1,3):
        try:
            jh_total_res_cn = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=(Confirmed%20%3E%200)%20AND%20(Country_Region%3D%27China%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins deaths for China
    for attempt_no in range(1,3):
        try:
            jh_dead_res_cn = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=(Confirmed%20%3E%200)%20AND%20(Country_Region%3D%27China%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Deaths%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins recoveries for China
    for attempt_no in range(1,3):
        try:
            jh_recovered_res_cn = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=(Confirmed%20%3E%200)%20AND%20(Country_Region%3D%27China%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Recovered%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins total time series CSV
    for attempt_no in range(1,3):
        try:
            jh_total_csv = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv',headers=headers, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins deaths time series CSV
    for attempt_no in range(1,3):
        try:
            jh_dead_csv = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv',headers=headers, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    # Get Johns Hopkins recoveries time series CSV
    for attempt_no in range(1,3):
        try:
            jh_recovered_csv = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv',headers=headers, timeout=15)
            break
        except:
            if attempt_no <= 3:
                print("Retrying")
            else:
                raise error

    jh_total_json = json.loads(jh_total_res.content.decode())
    jh_total = jh_total_json['features'][0]['attributes']['value']

    jh_dead_json = json.loads(jh_dead_res.content.decode())
    jh_dead = jh_dead_json['features'][0]['attributes']['value']

    jh_recovered_json = json.loads(jh_recovered_res.content.decode())
    jh_recovered = jh_recovered_json['features'][0]['attributes']['value']

    jh_total_json_cn = json.loads(jh_total_res_cn.content.decode())
    jh_total_cn = jh_total_json_cn['features'][0]['attributes']['value']

    jh_dead_json_cn = json.loads(jh_dead_res_cn.content.decode())
    jh_dead_cn = jh_dead_json_cn['features'][0]['attributes']['value']

    jh_recovered_json_cn = json.loads(jh_recovered_res_cn.content.decode())
    jh_recovered_cn = jh_recovered_json_cn['features'][0]['attributes']['value']

    return jh_total, jh_dead, jh_recovered, jh_total_cn, jh_dead_cn, jh_recovered_cn, jh_total_csv, jh_dead_csv, jh_recovered_csv