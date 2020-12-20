#imports
import discord
from discord import embeds
from discord.colour import Color
from textblob import TextBlob
from discord.ext import commands
import pandas as pd
import string
import os
import random
import glob

#intializing  the  bot 
client = commands.Bot(command_prefix = '!')

#events
@client.command(name="version")
async def version(context):
    
    myEmbed = discord.Embed(title="Current Version", description="The bot is in v1.0 currently")
    myEmbed.add_field(name="Version Code", value="v1.0.0",inline=False)
    myEmbed.add_field(name="Release Date",value="17th December 2020",inline=False)
    myEmbed.set_footer(text="Bot of IOTA's Server")
    myEmbed.set_author(name="Ankit Raibole")
    await context.message.channel.send(embed = myEmbed)

@client.command(name="kick",pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(context,member : discord.Member):
    await member.kick()
    await context.send(f'User {member.display_name} has been kicked')

@client.command(name="ban",pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(context,member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await context.send(f'User {member.display_name} has been baned')

@client.command(name="randimg")
async def ranimg(context):

    images =glob.glob("images/*.jpg")
    random_image = random.choice(images)
    await context.send(file=discord.File(random_image))

@client.command(name="create-reaction-post")
async def create_reatcion_post(context):

    embed = discord.Embed(title="Create Reaction Post",Color=0x8cc542)
    embed.set_author(name="Ankit Raibole")
    embed.add_field(name="Set Title", value="!reaction_set_title \"New Title\"")

    await context.send(embed=embed)
    await context.message.delete()

@client.event
async def on_ready(): 
    general_channel = client.get_channel(788403370854973516)
    await client.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game("free fire"))
    await general_channel.send("I am Available now!!!")
    
    
@client.event
async def on_disconnect():
    general_channel = client.get_channel(788403370854973516)
    await general_channel.send("Good Bye")

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f' Hi{member.name}, Welcome to Server IOTA! '
    )

@client.event
async def on_error(event,*args,**kwargs):
    with open('err.log','a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message : {args[0]}\n')
        else:
            raise event
        
@client.event
async def on_message(message):

    if message.author == client.user:
            
        return
    
    elif message.content.startswith("!store"):
        
        df = pd.read_csv(r"C:\Users\iota\Desktop\VScodes\project\Discord Bot\data.csv",index_col=0) 
        df = df.append({"Name":message.author,"Message":message.content},ignore_index=True)                                     
        df.to_csv(r"C:\Users\iota\Desktop\VScodes\project\Discord Bot\data.csv")
        await message.channel.send(f' {message.author} Your message has been store successfully ')
        
    elif message.content == 'raise-exception':
        
        raise discord.DicordException
    
    else:

        text = message.content
        print("message : " + message.content)
        polarity = TextBlob(text).sentiment.polarity
        
        if polarity < 0 and polarity > -0.5:
            
            await message.channel.send("Don't be Negative")
            
        elif polarity < -0.5:
            
            await message.channel.send("Next time u will be kicked")
            
        else :
            
            await message.channel.send("Thanks for being positive")
    
    await client.process_commands(message)
        
#running the bot script to make it online
client.run('Nzg4Mzk5MTY5MjQ1MTUxMjQy.X9i78Q.Bj_MBlMgTyxr_X5g_aF9x5q6PLs')
