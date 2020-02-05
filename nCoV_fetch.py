#!/usr/bin/python3

# 2019-nCoV Tracker v3.0-beta-1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-02-04
#
# A Twitter bot for posting information on the spread of the 2019-nCoV outbreak
#
# Uses Requests, Tweepy, and gspread libraries
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
    try:
        jh_total_res = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers, timeout=10)
        jh_total_json = json.loads(jh_total_res.content.decode())
        jh_total = jh_total_json['features'][0]['attributes']['value']
    except:
        jh_total = 0

    # Get Johns Hopkins deaths
    try:
        jh_dead_res = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Deaths%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers, timeout=10)
        jh_dead_json = json.loads(jh_dead_res.content.decode())
        jh_dead = jh_dead_json['features'][0]['attributes']['value']
    except:
        jh_dead = 0

    # Get Johns Hopkins recoveries
    try:
        jh_recovered_res = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Recovered%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&cacheHint=true',headers=headers, timeout=10)
        jh_recovered_json = json.loads(jh_recovered_res.content.decode())
        jh_recovered = jh_recovered_json['features'][0]['attributes']['value']
    except:
        jh_recovered = 0

    return jh_total, jh_dead, jh_recovered

# Fetch Tencent QQ News data
def get_qq(headers):
    # Get QQ
    try:
        qq_res = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5',headers=headers, timeout=10)
        qq_json = json.loads(qq_res.content.decode())
        qq_json_data = json.loads(qq_json['data'])
        qq_total = qq_json_data['chinaTotal']['confirm']
        qq_suspect = qq_json_data['chinaTotal']['suspect']
        qq_recovered = qq_json_data['chinaTotal']['heal']
        qq_dead = qq_json_data['chinaTotal']['dead']
    except:
        qq_total = 0
        qq_suspect = 0
        qq_recovered = 0
        qq_dead = 0

    return qq_total, qq_suspect, qq_recovered, qq_dead