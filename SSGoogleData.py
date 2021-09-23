#  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib to get google api pip install
import gspread, random, math
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from collections import defaultdict


class Val_Player:
    def __init__(self, Discord_Name, Player_IGN, Current_Rank):
        self.Discord_Name = Discord_Name
        self.Player_IGN = Player_IGN
        self.Current_Rank = Current_Rank


class Val_Team:
    def __init__(self):
        self.team_members = []

    def add_member(self, team_member):
        self.team_members.append(team_member)

    def update_member(self, arg, index):
        self.team_members[index] = arg

    def clear_team(self):
        self.team_members.clear()

    def __len__(self):
        return len(self.team_members)


def count_values(Dict_Values):
    values = 0
    if type(Dict_Values) == dict:
        for keys in Dict_Values.keys():
            if isinstance(Dict_Values[keys], (list, tuple, dict)):  # checking if the dictionary are any of these values
                v = count_values(Dict_Values[keys])
                values += v
            else:
                values += 1

    elif type(Dict_Values) == list or type(Dict_Values) == tuple:
        for keys in Dict_Values:
            if isinstance(keys, (list, tuple, dict)):
                v = count_values(Dict_Values)
                values += v
            else:
                values += 1

    return values


def count_columns():#add to column if the value is not None
    counter = 0

    for player in range(len(sheet.col_values(2))):
        if data[player][2] is not '':
            counter += 1

    return counter


def create_teams(All_Players):

    new_team = Val_Team()
    total_rankweight = 0
    new_team.add_member(total_rankweight)
    # try:
    while new_team.__len__() < 6:
        random_rank = random.choice(list(All_Players))  # gets one of the ranks from Iron-Radiant
        if random_rank == 'Radiant':
            pprint("you got radiant slut" + str(random_rank))
            length_of_rankedlist = len(All_Players[random_rank])

        else:
            random_rankedtier = random.choice(list(All_Players[random_rank]))  # gets random tier from 1-3
            length_of_rankedlist = len(All_Players[random_rank][random_rankedtier])

            while length_of_rankedlist <= 1:
                if random_rank == 'Radiant':
                    length_of_rankedlist = len(All_Players[random_rank])
                    pprint("you got radiant twice slut" + str(random_rank))
                    break
                else:
                    random_rank = random.choice(list(All_Players))
                    random_rankedtier = random.choice(list(All_Players[random_rank]))  # gets random tier from 1-3
                    length_of_rankedlist = len(All_Players[random_rank][random_rankedtier])

            random_playerindex = random.randint(1, (length_of_rankedlist - 1))  # helps pick a player from the tiers that is not the numerical value
            random_rankedplayer = All_Players[random_rank][random_rankedtier][random_playerindex]
            total_rankweight += All_Players[random_rank][random_rankedtier][0] #get the numerical value of the rank weight given statically
            new_team.update_member(total_rankweight,0)#update first item in new_team which is the rank weight
            new_team.add_member(random_rankedplayer.Player_IGN)
            All_Players[random_rank][random_rankedtier].remove(random_rankedplayer)#removes a person

    return new_team
    # except AttributeError as e:
    #     if e.message("'list' object has no attribute 'keys'"):
    #         if
    #         else:
    #         return


#     if e.message("'list' object has no attribute 'keys'"):
#         print("HA")
#     else:
#         print("bah")


# try:
#
# except AttributeError as e:
#     if e.message("'list' object has no attribute 'keys'"):
#         print("HA")
#     else:
#         print("bah")


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("token.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Scrub Series IV (Responses)").sheet1  # Open the spreadsheet

data = sheet.get_all_values()  # Get a list of all records

All_Players = {
    'Iron': {'1': [10], '2': [20], '3': [30]},
    'Bronze': {'1': [40], '2': [50], '3': [60]},
    'Silver': {'1': [70], '2': [80], '3': [90]},
    'Gold': {'1': [100], '2': [110], '3': [120]},
    'Platinum': {'1': [140], '2': [150], '3': [160]},
    'Diamond': {'1': [180], '2': [200], '3': [220]},
    'Immortal': {'1': [240], '2': [260], '3': [280]}
    #'Radiant': [300]
}

All_Teams = {}


for i in range(1, len(data)):

    try:
        Player_Info = Val_Player(data[i][1], data[i][2], data[i][3])
        Rank_Name, Rank_Number = data[i][3].split()

    except ValueError:  # when its missing Rank_number aka Radiant
        Rank_Name = data[i][3]
        Player_Info = Val_Player(data[i][1], data[i][2], Rank_Name)
        Rank_Number = None

    if Rank_Number is not None:
        All_Players[Rank_Name][Rank_Number].append(Player_Info)

    elif Rank_Name != '':
        All_Players[Rank_Name].append(Player_Info)

total_possible_teams = math.floor(count_columns()/5)

for i in range(total_possible_teams):

    All_Teams[i + 1] = create_teams(All_Players)
    pprint(All_Teams[i+1].team_members[0])

