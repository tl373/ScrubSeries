#  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib to get google api pip install
import gspread,time
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("token.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Scrub Series IV (Responses)").sheet1  # Open the spreadhseet

#data = sheet.get_all_records()  # Get a list of all records

#row = sheet.row_values(3)  # Get a specific row
#col = sheet.col_values(3)  # Get a specific column
#cell = sheet.cell(1,2).value  # Get the value of a specific cell
Players = {
    'iron':None,
    'bronze':None,
    'silver':None,
    'gold':None,
    'platinum':None,
    'diamond':None,
    'immortal':None,
    'radiant':None
}

numRows = sheet.row_count  # Get the number of rows in the sheet
numCol = sheet.col_count


for i in range(1,numCol):
    if sheet.cell(1, i).value != None: #sheet.cell(row,column)
        if sheet.cell(1,i).value == 'Current Rank': #column of the riot ID based off of rank
            colOfRanks = i #Column of the ranks associated by players

for j in range(1,numRows):
    if sheet.cell(j, colOfRanks).value is not None and sheet.cell(j, colOfRanks).value != 'Current Rank':
        colOfPlayers = colOfRanks-1
        pprint(sheet.cell(j, colOfPlayers).value)

        for ranks in Players.keys():
           if sheet.cell(j, colOfRanks).value in ranks:
               Players[ranks].append()




