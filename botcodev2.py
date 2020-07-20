import discord
from discord.ext import commands
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
async def troll(ctx):
    if ctx.author.id == jdm_id:
        def check(m):
            return m.author.id == jdm_id and "off" in m.content.lower()
        user = client.get_user(724027137832648724)
        while True:
            await user.send("CRINGE LMAO x")
            time.sleep(1)
            try:
                cancel = client.wait_for('message', check=check, timeout=20)
            except asyncio.TimeoutError:
                break
            else:
                pass

# ----------------------------------------------------------------------------------------------------------------------
# Run Bot Using Token

client.run(TOKEN)
