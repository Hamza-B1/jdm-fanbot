import discord
from discord.ext import commands
import discord.utils
import asyncio
import psycopg2
import datetime

# ----------------------------------------------------------------------------------------------------------------------
# Declaring Important Variables and Initialising Client Instance
main_client = discord.Client()
client = commands.Bot(command_prefix=';;')
client.remove_command('help')
jdm_id = 292626856509964288

# ----------------------------------------------------------------------------------------------------------------------
# Database Access set-up
uri = 'postgres://oshznwnnmoamqy:9b22fe118f0ade98da26f49717b8118e645941c468de967906d712420e44fd58@ec2-54-247-78-30.eu' \
      '-west-1.compute.amazonaws.com:5432/d1oetbi61398rd'
conn = psycopg2.connect(uri, sslmode='require')
cur = conn.cursor()

# ----------------------------------------------------------------------------------------------------------------------
# Loading Cogs And Printing Online Status in Log
cog_list = ['moderation']

for cog in cog_list:
    client.load_extension(f'cog_file.{cog}')
    print(f'{cog} loaded')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name='Borgar'))

# ----------------------------------------------------------------------------------------------------------------------
# Run bot using token

client.run("NDMzNjY4MzEzNTYzMDA0OTI4.XriBWg.7fb9u9IMEJocfIUFVdCCv5jlzg0")
