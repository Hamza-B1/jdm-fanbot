import discord
from discord.ext import commands
import psycopg2
import datetime

class Moderation(commands.Cog):
    """All Moderation Commands"""
    def __init__(self, client):

        """ Defining the client instance, giving database access"""
        self.client = client
        self.uri = 'postgres://oshznwnnmoamqy:9b22fe118f0ade98da26f49717b8118e645941c468de967906d712420e44fd58@ec2-54' \
                   '-247-78-30.eu-west-1.compute.amazonaws.com:5432/d1oetbi61398rd'
        self.conn = psycopg2.connect(self.uri, sslmode='require')
        self.cur = self.conn.cursor()

    @commands.command()
    async def initialise(self, ctx):
        if ctx.author.id == 292626856509964288:
            self.cur.execute('DROP TABLE test')
            self.cur.execute('CREATE TABLE mod_action (action_id SERIAL PRIMARY KEY, action_type varchar(10),'
                             ' member_id bigint, time timestamptz);')
            self.conn.commit()
            self.cur.execute('')
            await ctx.send('Database initialised')


def setup(client):
    client.add_cog(Moderation(client))
