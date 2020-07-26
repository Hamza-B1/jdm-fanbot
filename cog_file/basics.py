import discord
from discord.ext import commands
import psycopg2
import os
import pygal
import cairosvg
import io
from pygal.style import Style
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFont
import random


DB = os.environ['DATABASE_URL']
custom_style = Style(colors=('#00FFE8', '#4EEE4E', '#566AF3', '#BC0057'))

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
            role_specified = discord.utils.get(ctx.guild.roles, name=(role.title()))
            embed_list = discord.Embed(title=f"Role listing for {role.title()}",
                                       description=("\n".join(i.mention for i in role_specified.members)),
                                       colour=discord.Colour.dark_red())
            await ctx.send(embed=embed_list)
        else:
            embed2 = discord.Embed(title='', description=f'Role {role} not found', colour=discord.Colour.dark_red())
            await ctx.send(embed=embed2)

    @commands.command()
    async def yeardemo(self, ctx):
        names = ['University', 'Gap Year', 'Sixth Form', 'GCSE']
        year_chart = pygal.HorizontalBar(style=custom_style)
        year_chart.title = 'Server Members By Year'
        for i in names:
            year_chart.add(i, len(discord.utils.get(ctx.guild.roles, name=i).members))
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

    @commands.command()
    async def wojak(self, ctx, *, args):
        to_edit = Image.open(os.path.join("media", "angry.png"))
        draw = ImageDraw.Draw(to_edit)
        text = '\n'.join(wrap(args, 41))
        arial = ImageFont.truetype(os.path.join("media", "arial.ttf"), 28)
        draw.text((5, 5), text, fill='black', font=arial)
        file_obj = io.BytesIO()
        file_obj.seek(0)
        to_edit.save(file_obj, format='png')
        await ctx.send(file=discord.File(file_obj, filename="wojak.png"))


def setup(client):
    client.add_cog(Basics(client))
