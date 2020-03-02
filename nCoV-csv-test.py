import requests, pandas

jh_confirmed = requests.get('https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/time_series/time_series_2019-ncov-Confirmed.csv')

jh_confirmed_csv = pandas.read_csv(jh_confirmed)
print(jh_confirmed_csv)

jh_dead = requests.get('https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/time_series/time_series_2019-ncov-Deaths.csv')



jh_recovered = requests.get('https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/time_series/time_series_2019-ncov-Recovered.csv')



"""nCoV_dict = {}

for row in confirmed_list:
    nCoV_dict[row[1]] = {
        'province_data': {
            row[0]: [row[-1]]
        }
    }

print(nCoV_dict)

for row in dead_list:
    nCoV_dict[row[1]]['province_data'][row[0]].append(row[-1])

for row in recovered_list:
    nCoV_dict[row[1]]['province_data'][row[0]].append(row[-1])

print(nCoV_dict)"""