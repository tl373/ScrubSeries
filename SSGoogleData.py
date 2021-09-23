#  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib to get google api pip install
import gspread, time
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from collections import defaultdict

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("token.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Scrub Series IV (Responses)").sheet1  # Open the spreadhseet

data = sheet.get_all_values()  # Get a list of all records

Player_Ranks = {
    'Iron': {'1': [], '2': [], '3': []},
    'Bronze': {'1': [], '2': [], '3': []},
    'Silver': {'1': [], '2': [], '3': []},
    'Gold': {'1': [], '2': [], '3': []},
    'Platinum': {'1': [], '2': [], '3': []},
    'Diamond': {'1': [], '2': [], '3': []},
    'Immortal': [],
    'Radiant': []
}


for i in range(1, len(data)):

    try:
        Rank_Name, Rank_Number = data[i][3].split()

    except ValueError:# when its missing Rank_number aka immortal and radiant
        Rank_Name = data[i][3]
        Rank_Number = None

    if Rank_Number is not None:
        Player_Ranks[Rank_Name][Rank_Number].append(data[i][2])

    elif Rank_Name != '':
        Player_Ranks[Rank_Name].append(data[i][2])

pprint(Player_Ranks)