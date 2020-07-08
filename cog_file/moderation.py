import discord
from discord.ext import commands
import psycopg2
import datetime
import os
import asyncio
import concurrent.futures

DB = os.environ['DATABASE_URL']


class Moderation(commands.Cog):
    """All Moderation Commands"""

    def __init__(self, client):

        """Defining the client instance, giving database access"""

        self.client = client
        self.conn = psycopg2.connect(DB, sslmode='require')
        self.cur = self.conn.cursor()

    # ONLY FOR RESETTING DATABASE, EXPERIMENTAL PURPOSES
    @commands.command()
    async def initialise(self, ctx):
        if ctx.author.id == 292626856509964288:
            self.cur.execute('DROP TABLE mod_actions;')
            self.cur.execute('CREATE TABLE mod_actions (action_id SERIAL PRIMARY KEY, action_type varchar(12),'
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

        """Warn member and send action data to database. Cannot warn yourself or admins"""
        mod = False
        for i in member.roles:
            if i.name == 'Admin' or i.name == 'Mod':
                mod = True
        if member.id == ctx.author.id:
            await ctx.send('You cannot warn yourself!')
        elif mod:
            await ctx.send('You cannot warn this user!')
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
            self.cur.execute("SELECT * FROM mod_actions WHERE member_id = (%s) ;", (str(member.id),))
            x = self.cur.fetchall()
            if len(x) > 3:
                await member.kick()
                embed2 = discord.Embed(title='',
                                       description=f'Too many warnings, {member} was kicked')
                await ctx.send(embed=embed2)


    # @commands.command()
    # @commands.has_permissions(kick_members=True)
    # async def purgewarn(self, ctx, action_num):
    #
    #     """Clear warning from database"""
    #
    #     self.cur.execute("SELECT * FROM mod_actions WHERE action_id = (%s) AND action_type = 'warn'; ", (action_num,))
    #     x = self.cur.fetchall()
    #     if len(x) == 3:

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def inquire(self, ctx, action_num):
        self.cur.execute("SELECT * FROM mod_actions WHERE action_id = (%s); ", (action_num,))
        x = self.cur.fetchall()
        if len(x) == 0:
            embed = discord.Embed(description='Action not found. Did you type the wrong number?')
            await ctx.send(embed=embed)
        else:
            culprit = self.client.get_user(int(x[0][2]))
            mod = self.client.get_user(int(x[0][4]))
            embed_A = discord.Embed(title=f'Log for Action ID {action_num}', description='')
            embed_A.add_field(name=f'{culprit} {x[0][1]} by {mod}', value=f'{x[0][-1].strftime("%x at %H:%m")}')
            embed_A.set_thumbnail(url=culprit.avatar_url)
            embed_A.add_field(name='Reason', value=f'{x[0][3]}', inline=False)
            await ctx.send(embed=embed_A)
            await ctx.send('Would you like to edit the reason of this action? (yes/no)')

            # check function for use while waiting for input
            def check(m):
                return m.channel == ctx.channel and m.author.id == ctx.author.id

            # interface for editing action reason
            try:
                msg = await self.client.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send('Inquiry timed out.')
                return
            else:
                if 'yes' in msg.content:
                    await ctx.send('Please enter reason or type `;quit` to exit...')
                    try:
                        reason = await self.client.wait_for('message', check=check, timeout=45.0)
                    except concurrent.futures._base.TimeoutError:
                        await ctx.send('Inquiry timed out.')
                        return
                    else:
                        if reason.content.startswith(';quit'):
                            await ctx.send('Inquiry ended')
                            return
                        else:
                            self.cur.execute("UPDATE mod_actions SET reason = (%s) WHERE action_id = (%s);",
                                        (reason.content, action_num))
                            self.conn.commit()
                            await ctx.send('Inquiry updated. Thank you!')
                elif 'no' in msg.content:
                    await ctx.send('Inquiry ended')
                    return
                else:
                    await ctx.send('Please enter a valid choice. Inquiry ended')


def setup(client):
    client.add_cog(Moderation(client))
