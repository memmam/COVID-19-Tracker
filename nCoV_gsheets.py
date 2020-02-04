import gspread, pickle

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
    jh_sheet = client.open_by_key('1wQVypefm946ch4XDp37uZ-wartW4V7ILdg-qYiDXUHM')
    jh_worksheet = jh_sheet.get_worksheet(0)

    return jh_worksheet

# Build tweet list from Johns Hopkins CSSU data
def build_replies(datecode):
    jh_worksheet = get_jh_worksheet()

    # print(jh_worksheet.cell(1, 1).value)
    return []