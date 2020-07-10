import discord
from discord.ext import commands
import discord.utils
import asyncio
import psycopg2
import datetime
import os
import pygal
import cairosvg
import io

# ----------------------------------------------------------------------------------------------------------------------
# Declaring Important Variables and Initialising Client Instance
main_client = discord.Client()
client = commands.Bot(command_prefix=';;')
client.remove_command('help')
jdm_id = 292626856509964288
TOKEN = os.environ['TOKEN']
DB = os.environ['DATABASE_URL']

# ----------------------------------------------------------------------------------------------------------------------
# Database Access Set-up

conn = psycopg2.connect(DB, sslmode='require')
cur = conn.cursor()

# ----------------------------------------------------------------------------------------------------------------------
# Loading Available Cog Files and Printing Online Status in Log
cog_list = ['moderation']

for cog in cog_list:
    client.load_extension(f'cog_file.{cog}')
    print(f'{cog} loaded')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name='Borgar'))

# ----------------------------------------------------------------------------------------------------------------------
# Basic Commands

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def rolelist(ctx, *, role):
    """Gets a list of members of a specified role"""
    peeps = []
    if role.lower() in map(lambda x: x.name.lower(), ctx.guild.roles):
        for member in ctx.guild.members:
            for its_roles in member.roles:
                if its_roles.name.lower() == role.lower():
                    roles_match = its_roles
                    peeps.append(f'{member}')

        embed = discord.Embed(title=f'Role Listing for {roles_match} ', description='\n'.join(peeps),
                              colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)
    else:
        embed2 = discord.Embed(title='', description=f'Role {role} not found', colour=discord.Colour.dark_red())
        await ctx.send(embed=embed2)

@client.command()
async def yeardemo(ctx):
    year_chart = pygal.Bar()
    year_chart.title = 'Server Members By Year'
    year_chart.x_labels = "University", "Gap Year", "Sixth Form", "GCSE"
    x = year_chart.render_to_png()
    file_obj = io.BytesIO(x)
    await ctx.send(file=discord.File(file_obj, filename='chart.png'))

# ----------------------------------------------------------------------------------------------------------------------
# Run Bot Using Token

client.run(TOKEN)
