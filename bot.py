# pip install -U python-dotenv make sure to do so to make sure python can get env variables
# pip install -U discord.py install discord library
import os
import discord
import random
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
"""
@bot.command(name='score', help='Enter your score using !score <winning team> <score> (for example score will be 13-11 put in 13-11)')
async def set_score(ctx,*args):
    team_names = [
        'team1',
        'team2',
        'team3'
]

    for team in team_names:
        if args[0] == team:

"""


"""@bot.command(name='showTeam', help='shows what team you are on')
async def show_Team(ctx):
    
    await ctx.send(ctx.author.mention + " got: " + response + "!")
    
"""
bot.run(TOKEN)

