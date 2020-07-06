import discord
from discord.ext import commands
import psycopg2
import datetime


class Moderation(commands.Cog):
    """All Moderation Commands"""

    def __init__(self, client):

        """Defining the client instance, giving database access"""

        self.client = client
        self.uri = 'postgres://oshznwnnmoamqy:9b22fe118f0ade98da26f49717b8118e645941c468de967906d712420e44fd58@ec2-54' \
                   '-247-78-30.eu-west-1.compute.amazonaws.com:5432/d1oetbi61398rd'
        self.conn = psycopg2.connect(self.uri, sslmode='require')
        self.cur = self.conn.cursor()

    # ONLY FOR RESETTING DATABASE, EXPERIMENTAL PURPOSES
    @commands.command()
    async def initialise(self, ctx):
        if ctx.author.id == 292626856509964288:
            self.cur.execute('DROP TABLE mod_actions;')
            self.cur.execute('CREATE TABLE mod_actions (action_id SERIAL PRIMARY KEY, action_type varchar(10),'
                             ' member_id text, reason varchar(200), mod_id text, time timestamptz);')
            self.conn.commit()
            await ctx.send('Database initialised')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):

        """Purge messages command, defaults to 10"""

        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(title='', description=f'{amount} messages purged.')
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):

        """Message Logging (not connected to database)"""

        for channel in ctx.guild.text_channels:
            if channel.name == 'logs':
                embed = discord.Embed(title=f'Message Deleted in #{ctx.channel}',
                                      colour=discord.Colour.dark_red()
                                      )
                embed.add_field(name='Message Author', value=f'{ctx.author} | {ctx.author.id}', inline=False)
                embed.add_field(name='Content:', value=f'{ctx.content}', inline=True)
                embed.add_field(name=f'Message ID: ', value=f'{ctx.id}', inline=False)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):

        """Warn member and send action data to database. Cannot warn yourself"""

        if member.id == ctx.author.id:
            await ctx.send('You cannot warn yourself!')
        else:
            action = 'warn'
            self.cur.execute("INSERT INTO mod_actions VALUES (DEFAULT, %s, %s, %s, %s, %s);",
                             (action, member.id, reason, ctx.author.id, datetime.datetime.now()))
            self.conn.commit()
            self.cur.execute("SELECT MAX(action_id) FROM mod_actions;")
            self.cur.execute("SELECT * FROM mod_actions ORDER BY action_id DESC LIMIT 1;")
            value = self.cur.fetchone()
            embed = discord.Embed(
                title=f'{member} was warned',
                description='')
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f'Mods can inquire about this action using the '
                                  f'action ID: {value[0]}')
            embed.add_field(name='Reason', value=f'{reason}', inline=True)
            await ctx.send(embed=embed)
            self.cur.execute("SELECT * FROM mod_actions WHERE member_id = (%s) ;", (str(member.id), ))
            if len(self.cur.fetchall()) > 3:
                await member.kick()
                await ctx.send('Too many warnings, member was kicked')






def setup(client):
    client.add_cog(Moderation(client))
