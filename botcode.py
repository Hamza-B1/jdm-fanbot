import discord
from discord.ext import commands
import discord.utils
import random

main_client = discord.Client()

client = commands.Bot(command_prefix=';;')

client.remove_command('help')

jdm_id = 292626856509964288

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
        for channel in ctx.guild.text_channels:
            if channel.name == 'logs':
                embed2 = discord.Embed(title=f'{member} Kicked by {ctx.author}', description=f'Reason : {reason}')
                embed2.set_thumbnail(url=member.avatar_url)
                await channel.send(embed=embed2)


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
    for i in member.roles.name:
        if i.name == 'Muted':
            await ctx.send(f'{member} is already muted.')
            break
    else:
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(muted_role)
        await ctx.send(f'{member} was muted. Reason: {reason} \nShut the hell your mouth :sunglasses::metal:')


@client.command()
async def halaqa(ctx):
    for role in ctx.author.roles:
        if role.name == 'Halaqa':
            await ctx.send('You already have this role!')
            break
    halaqa_role = discord.utils.get(ctx.guild.roles, name='Halaqa')
    await ctx.author.add_roles(halaqa_role)
    await ctx.send('You now have the Halaqa role.')


@client.command()
async def students(ctx):
    for role in ctx.author.roles:
        if role.name == 'Students':
            await ctx.send('You already have this role!')
            break
    for role1 in ctx.guild.roles:
        if role1.name == 'Students':
            await ctx.author.add_roles(role1)
            await ctx.send('You now have the Student role.')





client.run("NDMzNjY4MzEzNTYzMDA0OTI4.XriBWg.7fb9u9IMEJocfIUFVdCCv5jlzg0")
