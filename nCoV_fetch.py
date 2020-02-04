import requests, json

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

# Build stats tweet from requested data
def build_stats_tweet(datecode):
    # request header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    # scrapers
    qq_total, qq_suspect, qq_recovered, qq_dead = get_qq(headers)
    jh_total, jh_dead, jh_recovered = get_jh(headers)

    # Construct statistics
    stats = (f"""{jh_total:,} (JH) / {qq_total:,} (QQ) cases\n"""
    f"""{qq_suspect:,} (QQ) suspected\n"""
    f"""{jh_dead:,} (JH) / {qq_dead:,} (QQ) deaths\n"""
    f"""{jh_recovered:,} (JH) / {qq_recovered:,} (QQ) recoveries\n\n"""
    f"""JH = Johns Hopkins\n"""
    f"""QQ = QQ News\n""")
    
    # Define hashtags
    with open ("hashtags.txt", "r") as hash_file:
        hashtags=hash_file.readline().replace('\n', '')
        hash_file.close()

    # Build statistics tweet
    stats_tweet = (f"""{datecode}\n\n"""
    f"""{stats}\n"""
    f"""Please retweet to spread awareness.\n\n"""
    f"""{hashtags}""")

    return stats_tweet