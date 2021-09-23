#  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib to get google api pip install
import gspread, random
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


def create_teams(All_Players,empty_dictcount):

    remove_playercount = count_values(All_Players)
    total_rankweight = 0
    # try:
    while empty_dictcount <= remove_playercount:
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
                    #pprint(random_rank)
                    random_rankedtier = random.choice(list(All_Players[random_rank]))  # gets random tier from 1-3
                    #pprint(random_rankedtier)
                    length_of_rankedlist = len(All_Players[random_rank][random_rankedtier])

        random_playerindex = random.randint(1, (length_of_rankedlist - 1))  # helps pick a player from the tiers that is not the numerical value
        #pprint(random_playerindex)
        #pprint(random_rank)
        random_rankedplayer = All_Players[random_rank][random_rankedtier][random_playerindex]
        total_rankweight += All_Players[random_rank][random_rankedtier][0] #get the numerical value of the rank weight given statically
        new_team.add_member(total_rankweight)
        new_team.add_member(random_rankedplayer.Player_IGN)
        All_Players[random_rank][random_rankedtier].remove(random_playerindex)
        remove_playercount = count_values(All_Players)
        #pprint(new_team.__len__())

        #pprint(All_Teams)

    #return All_Teams
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

empty_dictcount = count_values(All_Players) #when the dictionary All_players has no players in it

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

new_team = Val_Team()
team_number = 1
while new_team.__len__() >= 6:
    #All_Teams.setdefault(new_team)
    All_Teams[team_number] = new_team
    pprint(All_Teams)
    #print(team_number)
    team_number += 1 #add a new team


pprint(create_teams(All_Players,empty_dictcount))