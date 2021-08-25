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
    if not all(arg) and arg[0] != 'ban':
        for mapBans in arg[1:]:
            indextoBan = valorant_maps.index(mapBans.casefold())
            await ctx.send("Was banned: " + str(valorant_maps[indextoBan]).title())
            valorant_maps.pop(indextoBan)
            print(valorant_maps)

    response = random.choice(valorant_maps)
    await ctx.send(ctx.author.mention + " got: " + str(response).title() + "!")
    await ctx.send(file=discord.File(response + '.png'))


"""@bot.command(name='showTeam', help='shows what team you are on')
async def show_Team(ctx):
    
    await ctx.send(ctx.author.mention + " got: " + response + "!")
    
"""
bot.run(TOKEN)

