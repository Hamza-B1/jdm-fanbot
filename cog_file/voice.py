import discord
from discord.ext import commands
import psycopg2
import datetime
import os
import asyncio
# ----------------------------------------------------------------------------------------------------------------------
DB = os.environ['DATABASE_URL']
# ----------------------------------------------------------------------------------------------------------------------
class Voice(commands.Cog):
    """All Moderation Commands"""

    def __init__(self, client):

        """Defining the client instance, giving database access"""

        self.client = client
        self.conn = psycopg2.connect(DB, sslmode='require')
        self.cur = self.conn.cursor()

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

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

    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"Left {channel}")
        else:
            await ctx.send("Don't think I am in a voice channel")

def setup(client):
    client.add_cog(Voice(client))
