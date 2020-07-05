import discord
from discord.ext import commands
import discord.utils
import asyncio
import pytz
import psycopg2
import datetime

uri = 'postgres://oshznwnnmoamqy:9b22fe118f0ade98da26f49717b8118e645941c468de967906d712420e44fd58@ec2-54-247-78-30.eu' \
      '-west-1.compute.amazonaws.com:5432/d1oetbi61398rd'
main_client = discord.Client()
client = commands.Bot(command_prefix=';;')
client.remove_command('help')
jdm_id = 292626856509964288
conn = psycopg2.connect(uri, sslmode='require')
cur = conn.cursor()
@client.command()
async def db(ctx, member: discord.Member):
    if ctx.author.id == jdm_id:
        cur.execute("INSERT INTO test VALUES (%s, %s);", (member.id, datetime.datetime.now()))
        conn.commit()
        await ctx.send('Database updated')

@client.command()
async def dbtest(ctx):
    cur.execute('SELECT * FROM test;')
    member_id, dt_object = cur.fetchone()
    await ctx.send(member_id)
    await ctx.send(dt_object.strftime('%c'))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name='Borgar'))


@client.event
async def on_member_join(member):
    if member.guild.id == 679781666423570480:
        channel = client.get_channel(715991568179265536)
        await channel.send(f'As salaam alaykum {member.mention}! To gain access to the rest of the server, '
                           f'you need to talk here for a little while '
                           f'to level up. Enjoy your stay :sunglasses::metal:')


@client.event
async def on_message_delete(ctx):
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


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
async def diophantine(ctx, *, input):
    eq = ''.join(input.split())
    a = int(eq.split("x")[0])
    b_route = eq.split("+")
    b = int((b_route[1].split("y")[0]))
    c = int(eq.split("=")[1])
    embed = discord.Embed(
        title='Equation Decomposition',

        description=f'x coefficient = {a}\n y coefficient = {b}\n constant = {c}',
        colour=discord.Colour.dark_red()
    )
    await ctx.send(embed=embed)


# clear block
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(title='', description=f'{amount} messages purged.')
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        embed0 = discord.Embed(description='You cannot kick yourself.', colour=discord.Colour.dark_red())
        await ctx.send(embed=embed0)
        return
    else:
        await member.kick(reason=reason)
        embed = discord.Embed(title=f'{member} Kicked:', description=f'Reason : {reason}\n\n How '
                                                                     f'bout next time you join when you can '
                                                                     f'handle the Abdul Style :sunglasses::metal:'
                              , colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)

        embed2 = discord.Embed(title=f'{member} Kicked by {ctx.author}', description=f'Reason : {reason}')
        embed2.set_thumbnail(url=member.avatar_url)
        logs = discord.utils.get(ctx.guild.channels, name='logs')
        await logs.send(embed=embed2)


@client.command()
async def rolelist(ctx, *, role):
    peeps = []
    if role.lower() in map(lambda x: x.name.lower(), ctx.guild.roles):
        for member in ctx.guild.members:
            for its_roles in member.roles:
                if its_roles.name.lower() == role.lower():
                    roles_match = its_roles
                    peeps.append(f'{member}')

        embed = discord.Embed(title=f'Role Listing for {roles_match} ', description='\n'.join(peeps),
                              colour=discord.Colour.dark_red())
        await ctx.send(embed=embed)
    else:
        embed2 = discord.Embed(title='', description=f'Role {role} not found', colour=discord.Colour.dark_red())
        await ctx.send(embed=embed2)


@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if muted_role in member.roles:
        await ctx.send(f'{member} is already muted.')
    else:
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        embed_M = discord.Embed(title=f'{member} was muted.',
                                description=f'Reason: {reason}\nShut the hell your mouth :sunglasses::metal:')
        await member.add_roles(muted_role)
        await ctx.send(embed=embed_M)
        embed_L = discord.Embed(title=f'{member} Muted by {ctx.author}', description=f'Reason : {reason}',
                                colour=discord.Colour.dark_red())
        embed_L.set_thumbnail(url=member.avatar_url)
        logs = discord.utils.get(ctx.guild.channels, name='logs')
        await logs.send(embed=embed_L)


@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    logs = discord.utils.get(ctx.guild.channels, name='logs')
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f'{member} unmuted.')
        await logs.send(f'{member} unmuted.')
    else:
        await ctx.send('User isn\'t muted')


@client.command()
async def halaqa(ctx):
    if ctx.guild.id == 679781666423570480:
        for role in ctx.author.roles:
            if role.name == 'Halaqa':
                await ctx.send('You already have this role!')
                break
        halaqa_role = discord.utils.get(ctx.guild.roles, name='Halaqa')
        await ctx.author.add_roles(halaqa_role)
        await ctx.send('You now have the Halaqa role.')


@client.command()
async def study(ctx):
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


@client.command()
async def students(ctx):
    if ctx.guild.id == 679781666423570480:
        for role in ctx.author.roles:
            if role.name == 'Students':
                await ctx.send('You already have this role!')
                break
        for role1 in ctx.guild.roles:
            if role1.name == 'Students':
                await ctx.author.add_roles(role1)
                await ctx.send('You now have the Student role.')


abdulurl = 'https://cdn.discordapp.com/attachments/718254742702391317/719597802023551031/C2i3jNfXEAAelz7.png'
birburl = 'https://cdn.discordapp.com/attachments/665955692242534430/719184954776485982/20190720_070053_1.gif'
birb2url = 'https://cdn.discordapp.com/attachments/665955692242534430/719185105708515427/Snapchat-2142609126_1.gif'

locations = {0: ('Abdul Room', 'There\'s a car parked inside', abdulurl, {'west': 1}),
             1: ('Birb Room', 'Birb', birburl, {'east': 0, 'west': 2}),
             2: ('Birb Room 2', 'Another Birb', birb2url, {'east': 1})
             }


@client.command()
async def adventure(ctx):
    current = 0
    new_room = True
    while True:
        global locations
        if new_room:
            name, desc, url, directions = locations[current]
            embed_A = discord.Embed(title=f'You are currently in {name}.',
                                    description=f'{desc}\n'
                                                f'Available directions are: {", ".join(directions.keys())}.'
                                                f'\nType "quit" to exit the adventure.',
                                    colour=discord.Colour.dark_red())
            embed_A.set_image(url=url)
            await ctx.send(embed=embed_A)
            new_room = False

        def check(m):
            global locations
            return m.channel == ctx.channel and m.author.id == ctx.author.id

        try:
            msg = await client.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            break
        else:
            # noinspection PyUnboundLocalVariable
            if 'quit' in msg.content:
                break
            elif msg.content not in directions.keys():
                embed_B = discord.Embed(title='', description=f'{msg.content} is not a valid direction you cretin.',
                                        colour=discord.Colour.dark_red())
                await ctx.send(embed=embed_B)
            else:
                current = directions[msg.content]
                new_room = True
                continue
    embed_C = discord.Embed(title='', description='Adventure ended.', colour=discord.Colour.dark_red())
    await ctx.send(embed=embed_C)


client.run("NDMzNjY4MzEzNTYzMDA0OTI4.XriBWg.7fb9u9IMEJocfIUFVdCCv5jlzg0")
