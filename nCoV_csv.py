#!/usr/bin/env/python3

# Coronavirus Disease Tracker v10.5
# By Math Morissette (@TheYadda on Github)
# Last updated: 2020-04-13
#
# A Twitter/Discord bot for posting information on the spread of the COVID-19
# outbreak
#
# Uses Requests, Tweepy, pandas, discord-webhook, and matplotlib libraries
#
# File: nCoV_csv.py
# Purpose: CSV processing and graph generation for Coronavirus Disease Tracker

# For handling data for graphs
import pandas
import io
from datetime import date
from datetime import datetime

# For generating graphs
import matplotlib.spines as spines
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from matplotlib import dates

# Process CSV dataframes to return a dataframe for a specific country or set of
# countries
def process_csv(confirmed_df, dead_df, recovered_df, jh_dict, datestring,
                filter_country, filter_list, clip):
    # Create copy of dataframe to store result
    confirmed_df_aggregate = confirmed_df.copy()

    # If there is a filter list, sum the members of the list
    if filter_list != []:
        confirmed_df_aggregate = confirmed_df_aggregate[confirmed_df_aggregate \
                                 ['Country/Region'].isin(filter_list)]
        confirmed_df_aggregate = confirmed_df_aggregate.agg(sum)
        two_transpose = True

    # Special case: sum all countries if getting the world
    elif filter_country == 'World':
        confirmed_df_aggregate = confirmed_df_aggregate.agg(sum)
        two_transpose = True

    # General case: get only the country being asked for
    else:
        confirmed_df_aggregate.drop \
            (confirmed_df_aggregate[confirmed_df_aggregate['Country/Region'] \
             != filter_country].index, inplace = True)
        two_transpose = False

    # Repeat for dead and recovered dataframes
    dead_df_aggregate = dead_df.copy()
    if filter_list != []:
        dead_df_aggregate = dead_df_aggregate[dead_df_aggregate \
            ['Country/Region'].isin(filter_list)]
        dead_df_aggregate = dead_df_aggregate.agg(sum)
    elif filter_country == 'World':
        dead_df_aggregate = dead_df_aggregate.agg(sum)
    else:
        dead_df_aggregate.drop \
            (dead_df_aggregate[dead_df_aggregate['Country/Region'] \
             != filter_country].index, inplace = True)
    recovered_df_aggregate = recovered_df.copy()
    if filter_list != []:
        recovered_df_aggregate = recovered_df_aggregate[recovered_df_aggregate \
                                 ['Country/Region'].isin(filter_list)]
        recovered_df_aggregate = recovered_df_aggregate.agg(sum)
    elif filter_country == 'World':
        recovered_df_aggregate = recovered_df_aggregate.agg(sum)
    else:
        recovered_df_aggregate.drop \
            (recovered_df_aggregate[recovered_df_aggregate['Country/Region'] \
             != filter_country].index, inplace = True)

    # Add today, since time series data stops at yesterday
    confirmed_df_aggregate[datestring] = jh_dict[filter_country]['Confirmed']
    dead_df_aggregate[datestring] = jh_dict[filter_country]['Deaths']
    recovered_df_aggregate[datestring] = jh_dict[filter_country]['Recovered']

    # Adjust labels
    confirmed_df_aggregate['Country/Region'] = "Confirmed"
    dead_df_aggregate['Country/Region'] = "Deaths"
    recovered_df_aggregate['Country/Region'] = "Recovered"

    # Concatenate confirmed, dead, and recovered. Cases of multiple countries
    # will need to be transposed due to pandas auto-transpose behavior
    if two_transpose == True:
        df_aggregate = pandas.concat([confirmed_df_aggregate, \
                       dead_df_aggregate, recovered_df_aggregate], axis=1)
        df_aggregate = df_aggregate.transpose()
    else:
        df_aggregate = pandas.concat([confirmed_df_aggregate, \
                       dead_df_aggregate, recovered_df_aggregate], axis=0)
    df_aggregate.index = ['Confirmed', 'Deaths', 'Recovered']

    # Drop an extra column created by renaming the labels earlier
    df_aggregate = df_aggregate.drop(['Country/Region'], axis=1)

    # Convert dates in labels from strings to datetimes
    df_aggregate.columns = pandas.Index(map(lambda x : datetime.strptime \
                           (x,'%m/%d/%y'), df_aggregate.columns))

    # Dataframe is sideways, transpose it
    df_aggregate = df_aggregate.transpose()

    # Create active-case row
    df_aggregate['Active'] = df_aggregate['Confirmed'] \
                             - df_aggregate['Deaths'] \
                             - df_aggregate['Recovered']

    # Clip off too-old datapoints so graph doesn't have overlapping date labels
    if (df_aggregate.iloc[-79]['Confirmed'] \
            < df_aggregate.iloc[clip]['Confirmed']):
        df_aggregate = df_aggregate.iloc[clip:]
    else:
        df_aggregate = df_aggregate.iloc[-79:]

    return df_aggregate

# Generate subplots for 3x3 multigraph
def graph(df_aggregate, label_tail, fig, i):
    # Create axis to store graph
    ax = fig.add_subplot(3,3,i)

    # Background color
    ax.set_facecolor('mistyrose')

    # Grid color
    plt.grid(True, color='lightcoral')

    # Graph sides color
    for child in ax.get_children():
        if isinstance(child, spines.Spine):
            child.set_color('#CD5C5C')

    # Turn off scientific notation, give numbers commas, format dates
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().set_major_formatter(tick.FuncFormatter(
        lambda x, p: format(int(x), ',')))
    ax.get_xaxis().set_major_formatter(dates.DateFormatter('%-m/%-d'))

    # Set axis labels
    ax.set_ylabel(f'Cases {label_tail}')
    ax.set_xlabel('Date')

    # Create rules for major and minor x-axis ticks: major every week,
    # minor every day
    rule = dates.rrulewrapper(dates.DAILY, interval=7)
    rule_minor = dates.rrulewrapper(dates.DAILY, interval=1)
    days = dates.RRuleLocator(rule)
    days_minor = dates.RRuleLocator(rule_minor)

    # Create major and minor ticks: x-axis by rule above, y-axis auto-generated
    ax.xaxis.set_minor_locator(days_minor)
    ax.yaxis.set_minor_locator(tick.AutoMinorLocator())
    ax.xaxis.set_major_locator(days)
    ax.yaxis.set_major_locator(tick.AutoLocator())

    # Graph data lines
    plt.plot( 'Confirmed', data=df_aggregate, alpha=0.65)
    plt.plot( 'Active', data=df_aggregate, alpha=0.65)
    plt.plot( 'Deaths', data=df_aggregate, color='tab:red', alpha=0.65)
    plt.plot( 'Recovered', data=df_aggregate, color='tab:green', alpha=0.65)

    # Legend colors
    plt.legend(facecolor='lavenderblush', edgecolor='#f0a0a0')

    return ax

# Create global stats dataframes, defer to other functions for pulling out
# necessary data and making graphs
def generate_graphs(jh_csv_dict, jh_dict, header_arr):
    # Convert dictionary of CSV get requests into confirmed, dead, and
    # recovered dataframes
    confirmed_df = pandas.read_csv(io.StringIO(jh_csv_dict['Confirmed'] \
                   .decode('utf-8')))
    dead_df = pandas.read_csv(io.StringIO(jh_csv_dict['Deaths'].decode \
              ('utf-8')))
    recovered_df = pandas.read_csv(io.StringIO(jh_csv_dict['Recovered'] \
                   .decode('utf-8')))

    # Sum each country into a single column
    confirmed_df = confirmed_df.groupby('Country/Region', as_index=False) \
                   .agg(sum).drop(['Lat', 'Long'], axis=1)
    dead_df = dead_df.groupby('Country/Region', as_index=False).agg(sum) \
              .drop(['Lat', 'Long'], axis=1)
    recovered_df = recovered_df.groupby('Country/Region', as_index=False) \
                   .agg(sum).drop(['Lat', 'Long'], axis=1)

    # Get today's date, for adding today's data since the CSV data doesn't
    # include it
    today = date.today()
    datestring = today.strftime('%-m/%-d/%y')

    # Set text color for graphs; this needs to be here and not inside the graph
    # generator or else the first graph's text is black
    plt.rcParams['text.color'] = '#CD5C5C'
    plt.rcParams['axes.labelcolor'] = '#CD5C5C'
    plt.rcParams['xtick.color'] = '#CD5C5C'
    plt.rcParams['ytick.color'] = '#CD5C5C'

    # Iterate along the header array in 7-row blocks, generating
    # processed dataframes for a single country / group of countries
    length = len(header_arr)
    processed_arr = []
    for i in range(0, length, 5):
        processed_arr.append(
            process_csv(confirmed_df, dead_df, recovered_df, jh_dict, \
            datestring, header_arr[i + 1], header_arr[i + 4], \
            header_arr[i + 3]))

    # Create figure to store 3x3 graph grid
    fig = plt.figure(9, figsize=(18, 10.275))
    fig.patch.set_alpha(1)
    fig.patch.set_facecolor('mistyrose')

    # Generate subplots for the list of processed dataframes (range is hardcoded
    #  to prevent failure from user trying to generate more than 9 graphs)
    graphs = []
    for i in range(0,9):
        if header_arr[(5 * i) + 2] == 'Worldwide':
            graphs.append(
                graph(processed_arr[i], f"{header_arr[(5 * i) + 2]}", fig,
                i + 1))
        elif header_arr[(5 * i) + 2] in \
                ['EU + United Kingdom', 'United States', 'United Kingdom']:
            graphs.append(
                graph(processed_arr[i], f"in the {header_arr[(5 * i) + 2]}", \
                fig, i + 1))
        else:
            graphs.append(graph(processed_arr[i], \
                f"in {header_arr[(5 * i) + 2]}", fig, i + 1))

    # Get rid of the thick borders around each graph
    fig.tight_layout()

    # Get ylabels removed by tight_layout on graphs 1-6 back
    for i in range(0,6):
        graphs[i].xaxis.set_tick_params(labelbottom=True)

    # Save graph as image and close dataframe to free memory
    fig.savefig("graph.png", facecolor=fig.get_facecolor(), edgecolor='none', \
                dpi=375)
    plt.close()

    # Logger output: generated dataframes
    pandas.set_option("display.max_rows", None)
    for i in range(0,9):
        print(processed_arr[i])
    print("\n")