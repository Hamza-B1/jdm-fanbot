import discord
from discord.ext import commands
import discord.utils

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
    await ctx.send(f'{amount} messages purged.')


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
@commands.has_permissions(manage_messages=True)
async def silence(ctx, member: discord.Member, *, reason=None):
    for role in ctx.guild.roles:
        if role.name == 'Muted':
            await member.add_roles(role)
    for role1 in ctx.guild.roles:
        if role1.name == 'Zumalaa':
            await member.remove_roles(role1)
    await ctx.send(f'{member} was muted. Reason: {reason}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def unsilence(ctx, member: discord.Member):
    for role in ctx.guild.roles:
        if role.name == 'Muted':
            await member.remove_roles(role)
    for role1 in ctx.guild.roles:
        if role1.name == 'Zumalaa':
            await member.add_roles(role1)
    await ctx.send(f'{member} was unmuted.')


@client.command()
async def halaqa(ctx):
    for role in ctx.author.roles:
        if role.name == 'Halaqa':
            await ctx.send('You already have this role!')
            return
    for role1 in ctx.guild.roles:
        if role1.name == 'Halaqa':
            await ctx.author.add_roles(role1)
            await ctx.send('You now have the Halaqa role.')


@client.command()
async def students(ctx):
    for role in ctx.author.roles:
        if role.name == 'Students':
            await ctx.send('You already have this role!')
            return
    for role1 in ctx.guild.roles:
        if role1.name == 'Students':
            await ctx.author.add_roles(role1)
            await ctx.send('You now have the Student role.')


client.run("NDMzNjY4MzEzNTYzMDA0OTI4.XriBWg.7fb9u9IMEJocfIUFVdCCv5jlzg0")
