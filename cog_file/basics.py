import discord
from discord.ext import commands
import psycopg2
import os
import asyncio
import pygal
import cairosvg
import io

DB = os.environ['DATABASE_URL']


class Basics(commands.Cog):
    """Basic Server Commands"""

    def __init__(self, client):

        """Defining the client instance, giving database access"""

        self.client = client
        self.conn = psycopg2.connect(DB, sslmode='require')
        self.cur = self.conn.cursor()

    @commands.command()
    async def rolelist(self, ctx, *, role):
        """Gets a list of members of a specified role"""
        if role.lower() in map(lambda x: x.name.lower(), ctx.guild.roles):
            # for member in ctx.guild.members:
            #     for its_roles in member.roles:
            #         if its_roles.name.lower() == role.lower():
            #             roles_match = its_roles
            #             peeps.append(f'{member}')

            # embed = discord.Embed(title=f'Role Listing for {roles_match} ', description='\n'.join(),
            #                       colour=discord.Colour.dark_red())
            # await ctx.send(embed=embed)
            role_specified = discord.utils.get(ctx.guild.roles, name=(role.title()))
            embed_list = discord.Embed(title=f"Role listing for {role.title()}", description=("\n".join(i.mention for i in role_specified.members)))
            await ctx.send(embed=embed_list)
        else:
            embed2 = discord.Embed(title='', description=f'Role {role} not found', colour=discord.Colour.dark_red())
            await ctx.send(embed=embed2)

    @commands.command()
    async def yeardemo(self, ctx):
        uni = discord.utils.get(ctx.guild.roles, name='University')
        gy = discord.utils.get(ctx.guild.roles, name='Gap Year')
        sf = discord.utils.get(ctx.guild.roles, name='Sixth Form')
        g = discord.utils.get(ctx.guild.roles, name='GCSE')
        year_chart = pygal.HorizontalBar()
        year_chart.title = 'Server Members By Year'
        year_chart.add("University", len(uni.members))
        year_chart.add("Gap Year", len(gy.members))
        year_chart.add("Sixth Form", len(sf.members))
        year_chart.add("GCSE", len(g.members))
        x = year_chart.render_to_png()
        file_obj = io.BytesIO(x)
        await ctx.send(file=discord.File(file_obj, filename='chart.png'))

    @commands.command()
    async def study(self, ctx):
        study_role = discord.utils.get(ctx.guild.roles, name='studying')
        if study_role in ctx.author.roles:
            await ctx.author.remove_roles(study_role)
            embed1 = discord.Embed(title='', description='Studying role removed. Did you do enough work :thinking:')
            await ctx.send(embed=embed1)
        else:
            await ctx.author.add_roles(study_role)
            embed = discord.Embed(title='',
                                  description='You now have the Studying role. Go get that bread :sunglasses::metal:')
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Basics(client))
