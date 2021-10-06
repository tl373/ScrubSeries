# pip install -U python-dotenv make sure to do so to make sure python can get env variables
# pip install -U discord.py install discord library
import os
import discord
import random
import redis
from SSGoogleData import *
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
redis_server = redis.Redis()
TOKEN = str(redis_server.get('DISCORD_TOKEN').decode('utf-8'))
client = discord.Client()

bot = commands.Bot(command_prefix='!')

@bot.command(name='randommap', help='Gives a random map name. To ban specific maps add ban after !randommap')
async def random_map(ctx,*arg):
    valorant_maps = [
        'Haven',
        'Ascent',
        'Icebox',
        'Bind',
        'Breeze',
        'Split'
    ]
    # if ctx.author.bot == True:
    #     await ctx.send("test")
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

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    await bot.invoke(ctx)

All_Teams = print_teams_to_Discord()

@bot.command(name='myTeam', help='shows what team you are on')
async def myTeam(ctx):
    my_team_list = []
    for i in range(1, len(All_Teams.keys()) + 1):
        length_of_team = 0
        while length_of_team != len(All_Teams[i].team_members):
            if str(ctx.message.author) == All_Teams[i].team_members[length_of_team][1]:
                for player_ign in range(len(All_Teams[i].team_members)):
                    my_team_list.append(str(':') + str(All_Teams[i].team_members[player_ign][2]) + str(': ') + str(All_Teams[i].team_members[player_ign][0]))
                    formated_my_team_list = "\n".join(my_team_list)

                await ctx.send(ctx.author.mention + " is a part of team " + str(i) + " which has the members \n"
                               + formated_my_team_list)
                return
            else:
                length_of_team += 1

    await ctx.send(ctx.author.mention + " is a part of team is not a part of a team")

@bot.command(name='allTeams', help='shows all teams created')
async def allTeams(ctx):

    for i in range(1,len(All_Teams.keys())+1):
        all_teams_list = []
        if All_Teams[i].team_members is not None:
            for j in range(len(All_Teams[i].team_members)):
                all_teams_list.append(str(':') + str(All_Teams[i].team_members[j][2]) + str(': ') + str(All_Teams[i].team_members[j][0]))
                print_formatted_list = "\n".join(all_teams_list)
        await ctx.send("Team " + str(i) + " has the members \n" + print_formatted_list)


bot.run(TOKEN)

