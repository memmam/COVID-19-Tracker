#!/usr/bin/python3

# Coronavirus Disease Tracker v6.0-b1
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-03-23
#
# A Twitter bot for posting information on the spread of the COVID-19 outbreak
#
# Uses Requests, Tweepy, and pandas libraries
#
# File: nCoV_csv.py
# Purpose: CSV processing for Coronavirus Disease Tracker

# import pandas

def generate_graphs(jh_total_csv, jh_dead_csv, jh_recovered_csv):
    allcountries_graph = 0
    china_graph = 0
    not_china_graph = 0
    return allcountries_graph, china_graph, not_china_graph