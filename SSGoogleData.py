#  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib to get google api pip install
import gspread, random, math
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


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

    def add_weight(self, arg):
        self.team_members[0] += arg

    def clear_team(self):
        self.team_members.clear()

    def __len__(self):
        return len(self.team_members)


def count_columns():  # add to column if the value is not None
    counter = 0

    for player in range(len(sheet.col_values(2))):
        if data[player][2] is not '':
            counter += 1

    return counter


def iterate_dict(dictionary):
    for key, value in list(dictionary.items()):
        # Check if value is of dict type
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for pair in iterate_dict(value):
                yield (key, *pair)
        else:
            # If value is not dict type then yield the value
            yield (key, value)


def remove_empty_ranks():
    for pair in iterate_dict(All_Players):
        rank_to_delete = str(pair[0])
        tier_to_delete = str(pair[1])
        try:
            print(str(pair[2][1].Player_IGN))

        except IndexError:
            if rank_to_delete is not 'Radiant':
                del All_Players[rank_to_delete][tier_to_delete]
            else:
                del All_Players[rank_to_delete]

            if rank_to_delete is not 'Radiant' and len(All_Players[rank_to_delete]) == 0:
                del All_Players[rank_to_delete]

    return All_Players


def highest_possible_ranked_player(All_Players):
    highest_possible_weight = 0
    weight_to_compare = 0
    rank_keys_list = list(All_Players)
    if 'Radiant' in All_Players:
        highest_possible_weight = 300
        rank_key = 'Radiant'
        return highest_possible_weight, rank_key

    for rank_index in range(len(All_Players.keys())-1,-1,-1):
        rank_key = rank_keys_list[rank_index] # the key for highest rank
        rank_tier_keys_list = list(All_Players[rank_key])#list of all the rank tiers in given rank_key

        for rank_tier_index in range(len(All_Players[rank_key])-1, -1,-1):
            rank_tier_key = rank_tier_keys_list[rank_tier_index] # showing all the keys in rank tier (aka all the tiers in Diamond = 1,2,3)

            if len(All_Players) == 1:
                highest_rank_key = rank_key
                highest_rank_tier = rank_tier_key
                highest_possible_weight = All_Players[rank_key][rank_tier_key][0]

            elif weight_to_compare >= All_Players[rank_key][rank_tier_key][0]:
                highest_rank_key = temp_rank_key
                highest_rank_tier = temp_rank_tier_key
                highest_possible_weight = weight_to_compare

            else:
                weight_to_compare = All_Players[rank_key][rank_tier_key][0]
                temp_rank_key = rank_key
                temp_rank_tier_key = rank_tier_key


    return highest_possible_weight, highest_rank_key, highest_rank_tier



def find_player(All_Players):  # traverse All_Players dictionary and get the highest value

    highest_possible_rank = highest_possible_ranked_player(All_Players)
    weight = highest_possible_rank[0]
    length_of_rankedlist = len(All_Players[highest_possible_rank[1]][highest_possible_rank[2]])
    random_playerindex = random.randint(1, length_of_rankedlist-1)
    random_ranked_player = All_Players[highest_possible_rank[1]][highest_possible_rank[2]][random_playerindex]
    All_Players[highest_possible_rank[1]][highest_possible_rank[2]].remove(random_ranked_player)
    remove_empty_ranks()

    return weight, random_ranked_player.Player_IGN, random_ranked_player.Discord_Name


def create_teams(All_Players,All_Teams):

    new_teams = {}
    total_rank_weight = 0

    for i in range(1,len(All_Teams.keys())+1):
        new_team = Val_Team()
        new_team.add_member(total_rank_weight)
        player_info = find_player(All_Players)
        Player_IGN_and_Discord = []
        Player_IGN_and_Discord.append(player_info[1])
        Player_IGN_and_Discord.append(player_info[2])
        new_team.add_weight(player_info[0])
        new_team.add_member(Player_IGN_and_Discord)
        new_teams[i] = new_team
        remove_empty_ranks()

    i = 1

    while True:
        if len(All_Players) == 0:
            for final_key in range(1, len(All_Teams.keys()) + 1):
                if len(new_teams[final_key].team_members) <= 6:
                    All_Teams[final_key] = new_teams[final_key]
                    #pprint(All_Teams[final_key])

                else:
                    new_teams[final_key].team_members.pop()
                    new_teams[final_key].add_weight(player_info[0]*-1)
                    All_Teams[final_key] = new_teams[final_key]
            return All_Teams
        elif i == 6:
            i = 1
        else:
            player_info = find_player(All_Players)
            Player_IGN_and_Discord = []
            Player_IGN_and_Discord.append(player_info[1])
            Player_IGN_and_Discord.append(player_info[2])
            new_teams[i].add_weight(player_info[0])
            new_teams[i].add_member(Player_IGN_and_Discord)
            remove_empty_ranks()
            i += 1


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
    'Immortal': {'1': [240], '2': [260], '3': [280]},
    'Radiant': [300]
}


def print_teams_to_Discord():
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

    total_possible_teams = math.floor(count_columns() / 5)
    All_Team_Numbers = []
    All_Teams = {}

    for i in range(total_possible_teams):
        All_Team_Numbers.append(i + 1)

    All_Teams = dict.fromkeys(All_Team_Numbers)
    remove_empty_ranks()

    All_Teams = create_teams(All_Players,All_Teams)
    for i in range(1, len(All_Teams.keys()) + 1):
        if isinstance(All_Teams[i].team_members[0], int):
            All_Teams[i].team_members.pop(0)


    return All_Teams

# All_Teams = print_teams_to_Discord()
#
# for i in range(1,len(All_Teams.keys())+1):
#     if isinstance(All_Teams[i].team_members[0], int):
#         All_Teams[i].team_members.pop(0)
#
#     pprint(All_Teams[i].team_members)

