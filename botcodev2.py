import discord
from discord.ext import commands
import psycopg2
import os
import time
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
cog_list = ['moderation', 'basics']

for cog in cog_list:
    client.load_extension(f'cog_file.{cog}')
    print(f'{cog} loaded')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name='Special thanks to Abdul C'))

# ----------------------------------------------------------------------------------------------------------------------
# Basic Commands

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def jointest(ctx):
    ch = ctx.author.voice.channel
    voice_client = client.voice_clients.in_server(ctx.guild)
    await voice_client.join_channel(ch)
    time.sleep(3)
    await voice_client.leave_channel(ch)

# ----------------------------------------------------------------------------------------------------------------------
# Run Bot Using Token

client.run(TOKEN)
