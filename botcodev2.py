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
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f"Joined {channel}")


@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")

# ----------------------------------------------------------------------------------------------------------------------
# Run Bot Using Token

client.run(TOKEN)
