import discord
from discord.ext import commands
import psycopg2
import datetime
import time
import os
import asyncio
import concurrent.futures  # not sure why still using this for the timeout exception but it works, do not edit unless

# needed

# ----------------------------------------------------------------------------------------------------------------------
# Defining Embeds
id_error = discord.Embed(title='ID Error', description='Action not found. Did you provide the correct ID?',
                         colour=discord.Colour.dark_red())

# ----------------------------------------------------------------------------------------------------------------------
DB = os.environ['DATABASE_URL']


# ----------------------------------------------------------------------------------------------------------------------

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
            self.cur.execute(
                'CREATE TABLE chrono_tasks (action_id SERIAL PRIMARY KEY, action_type varchar(20), time_start varchar(100), time_end varchar(100));')
            self.conn.commit()
            await ctx.send('Database initialised')

    @commands.Cog.listener()
    async def on_message(self, message):
        def check(m):
            return m.author == message.author and m.author.id != 433668313563004928
        try:
            msg = await self.client.wait_for('message', check=check, timeout=1.8)
            await message.delete()
            await msg.delete()
            try:
                new_msg = await self.client.wait_for('message', check=check, timeout=1.8)
                await new_msg.author.add_roles(discord.utils.get(message.guild.roles, name='Muted'))
            except asyncio.TimeoutError:
                pass
        except asyncio.TimeoutError:
            pass
        await self.client.process_commands()

    @commands.command()
    async def initialise(self, ctx):
        if ctx.author.id == 292626856509964288:
            self.cur.execute("DROP TABLE chrono_tasks")
            self.cur.execute(
                'CREATE TABLE chrono_tasks (action_type varchar(20), time_start varchar(100), time_end varchar(100));')
            self.conn.commit()
            await ctx.send('Database initialised')


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):

        """Purge messages command, defaults to 10"""

        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(title='', description=f'{amount} messages purged in {ctx.channel} by {ctx.author}.')
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
            await ctx.send("You cannot warn yourself.")
        elif mod:
            await ctx.send("You cannot warn this user.")
        else:
            self.cur.execute("INSERT INTO mod_actions VALUES (DEFAULT, 'warn', %s, %s, %s, %s);",
                             (member.id, reason, ctx.author.id, datetime.datetime.now()))
            self.conn.commit()
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

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def purgewarn(self, ctx, action_num, *, new_reason=None):

        """Clear warning from database"""

        self.cur.execute("SELECT * FROM mod_actions WHERE action_id = (%s) AND action_type = 'warn'; ", (action_num,))
        x = self.cur.fetchall()
        # check if warning exists then send purge to logs.
        if len(x):
            self.cur.execute("DELETE FROM mod_actions WHERE action_id = (%s) AND action_type = 'warn';", (action_num,))
            self.conn.commit()
            embed = discord.Embed(title='', description=f"Warning {action_num} removed by {ctx.author}.")
            await ctx.send(embed=embed)
            logs = discord.utils.get(ctx.guild.channels, name='logs')
            culprit = self.client.get_user(int(x[0][2]))
            mod = self.client.get_user(int(x[0][4]))
            embed_A = discord.Embed(title=f'Action ID {action_num}',
                                    description=f"Warning {action_num} removed by {ctx.author}.",
                                    colour=discord.Colour.dark_red())
            embed_A.add_field(name=f'{culprit} {x[0][1]} by {mod}', value=f'{x[0][-1].strftime("%x at %H:%m")}')
            embed_A.set_thumbnail(url=culprit.avatar_url)
            embed_A.add_field(name='Reason', value=f'{x[0][3]}', inline=False)
            embed_A.add_field(name='Reason For Purge', value=f"{new_reason}")
            await logs.send(embed=embed_A)
        else:
            await ctx.send(embed=id_error)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def inquire(self, ctx, action_num):
        self.cur.execute("SELECT * FROM mod_actions WHERE action_id = (%s); ", (action_num,))
        x = self.cur.fetchall()
        if len(x) == 0:
            await ctx.send(embed=id_error)
        else:
            culprit = self.client.get_user(int(x[0][2]))
            mod = self.client.get_user(int(x[0][4]))
            embed_A = discord.Embed(title=f'Log for Action ID {action_num}', description='',
                                    colour=discord.Colour.dark_red())
            embed_A.add_field(name=f'{culprit} {x[0][1]} by {mod}', value=f'{x[0][-1].strftime("%x at %H:%m")}')
            embed_A.set_thumbnail(url=culprit.avatar_url)
            embed_A.add_field(name='Reason', value=f'{x[0][3]}', inline=False)
            await ctx.send(embed=embed_A)
            await ctx.send(
                'Would you like to edit the reason of this action? If you enter an invalid response, the inquiry will '
                'terminate.')

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
                if 'yes' in msg.content.lower():
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
                            await ctx.send(f"Inquiry updated. Thank you! New reason: {reason.content}")
                elif 'no' in msg.content.lower():
                    await ctx.send("Inquiry ended")
                    return
                else:
                    pass

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warnlist(self, ctx, member_id):

        """Gets a list of warnings that a member has"""

        s_user = self.client.get_user(int(member_id))
        self.cur.execute("SELECT * FROM mod_actions WHERE action_type = 'warn' and member_id = (%s);", (member_id,))
        x = self.cur.fetchall()
        embed = discord.Embed(title=f'Warnings for {s_user}', description='', colour=discord.Colour.dark_red())
        for warn in x:
            embed.add_field(name=f"ID: {warn[0]} | Reason:", value=f"{warn[3]}\n{warn[5].strftime('%x at %H:%m')}",
                            inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        mod = False
        for i in member.roles:
            if i.name == 'Admin' or i.name == 'Mod':
                mod = True
        if member.id == ctx.author.id:
            await ctx.send("You can't kick yourself.")
        elif mod:
            await ctx.send("You can't kick this user.")
        else:
            self.cur.execute("INSERT INTO mod_actions VALUES (DEFAULT, 'kick', %s, %s, %s, %s);",
                             (member.id, reason, ctx.author.id, datetime.datetime.now()))
            self.conn.commit()
            self.cur.execute("SELECT * FROM mod_actions ORDER BY action_id DESC LIMIT 1;")
            value = self.cur.fetchone()
            embed = discord.Embed(
                title=f'{member} was kicked',
                description='')
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f'Mods can inquire about this action using the '
                                  f'action ID: {value[0]}')
            embed.add_field(name='Reason', value=f'{reason}', inline=True)
            await ctx.send(embed=embed)
            await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *args):
        mod = False
        muted = False
        for i in member.roles:
            if i.name == 'Muted':
                muted = True
        for i in member.roles:
            if i.name == 'Admin' or i.name == 'Mod':
                mod = True
        if member.id == ctx.author.id:
            await ctx.send("You cannot mute yourself.")
        elif mod:
            await ctx.send("You cannot mute this user.")
        elif muted:
            await ctx.send("This user is already muted.")
        else:
            reason = []
            days, hrs, mins, secs = 0, 0, 0, 0
            for i in range(len(args)):
                if args[i] == "-d":
                    try:
                        days = int(args[i + 1])
                    except ValueError:
                        await ctx.send("Please enter valid number of days.")
                        return
                elif args[i] == "-h":
                    try:
                        hrs = int(args[i + 1])
                    except ValueError:
                        await ctx.send("Please enter valid number of hours.")
                        return
                elif args[i] == "-m":
                    try:
                        mins = int(args[i + 1])
                    except ValueError:
                        await ctx.send("Please enter valid number of minutes")
                        return
                elif args[i] == "-s":
                    try:
                        secs = int(args[i + 1])
                    except ValueError:
                        await ctx.send("Please enter a valid number of seconds")
                        return
                elif args[i] != ("-d" or "-h" or "-m" or "-s"):
                    if i - 1 < 0:
                        reason.append(args[i])
                    elif args[i - 1].isalpha():
                        reason.append(args[i])
            if not reason:
                reason = None
            else:
                reason = " ".join(reason)
            total = int(days) * 24 * 3600 + int(hrs) * 3600 + int(mins) * 60 + int(secs)
        await ctx.send(total)
        await ctx.send(reason)


def setup(client):
    client.add_cog(Moderation(client))
