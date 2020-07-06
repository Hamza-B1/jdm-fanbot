import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cogtest(self, ctx):
        await ctx.channel.send('Cog is working')


def setup(client):
    client.add_cog(Moderation(client))
