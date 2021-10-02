# pip install -U python-dotenv make sure to do so to make sure python can get env variables
# pip install -U discord.py install discord library
import os
import discord
import random
from SSGoogleData import *
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='randommap', help='Gives a random map name. To ban specific maps add ban after !randommap')
async def random_map(ctx,*arg):
    valorant_maps = [
        'haven',
        'ascent',
        'icebox',
        'bind',
        'breeze',
        'split'
    ]
    if len(arg) >= 2 and arg[0].strip() == 'ban':
        for mapBans in arg[1:]:
            indextoBan = valorant_maps.index(mapBans.casefold())
            await ctx.send("Was banned: " + str(valorant_maps[indextoBan]).title())
            valorant_maps.pop(indextoBan)
            response = random.choice(valorant_maps)
            await ctx.send(ctx.author.mention + " got: " + str(response).title() + "!")
            await ctx.send(file=discord.File(response + '.png'))
            print(valorant_maps)
    elif len(arg) == 1:
        if arg[0].strip() != 'ban':
            await ctx.send(arg[0] + " is not ban please put the argument ban")
            return
        else:
            await ctx.send("Not enough arguments put in only " + len(arg) + " was put in please put the following ban <map name>")
            return

    response = random.choice(valorant_maps)
    await ctx.send(ctx.author.mention + " got: " + str(response).title() + "!")
    await ctx.send(file=discord.File(response + '.png'))

All_Teams = print_teams_to_Discord()

@bot.command(name='myTeam', help='shows what team you are on')
async def myTeam(ctx):
    my_team_list = []
    for i in range(1, len(All_Teams.keys()) + 1):
        length_of_team = 0
        while length_of_team != len(All_Teams[i].team_members):
            if str(ctx.message.author) == All_Teams[i].team_members[length_of_team][1]:
                for player_ign in range(len(All_Teams[i].team_members)):
                    my_team_list.append(All_Teams[i].team_members[player_ign][0])

                await ctx.send(ctx.author.mention + " is a part of team " + str(i) + " which has the members "
                               + str(my_team_list))
                return
            else:
                length_of_team += 1

    await ctx.send(ctx.author.mention + " is a part of team is not a part of a team")


bot.run(TOKEN)

