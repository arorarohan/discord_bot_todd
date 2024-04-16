import discord
from discord.ext import commands
from keys_ids import *

#set our intents
intents = discord.Intents.all()
intents.members = True


#initialize the client, set the prefix for bot commands to be 'todd '.
client = commands.Bot(command_prefix='todd ', intents=intents)


######################################################################################################
#########################################EVENTS######################################################
######################################################################################################

#define what the bot does when it starts up, for now just show that it has started via the terminal
@client.event
async def on_ready():
    #this is printed to the terminal for the host, not visible to the user
    print("The bot is now ready for use!")
    print("------------------------------------")


#this decorator will be used whenever we want our bot to respond to an event that happens in the server. In this case, when a new member joins.
@client.event
async def on_member_join(member):
    
    #get the channel that we want to send our welcome message in
    channel = client.get_channel(WELCOME_CHANNEL)

    #then send our message in that channel, and print that we have done so to the terminal.
    await channel.send("Yo dog, nice to meet you dog. I'm Todd. the dog. woof bark woof.")
    print("Welcomed a new member!")


#say something when a member is removed
@client.event
async def on_member_remove(member):

    #once again, first get the channel, then send our message there and tell the host it's been done.
    channel = client.get_channel(WELCOME_CHANNEL)
    await channel.send("Goobye. Guess you weren't a real dog. I shouldn't have called you dog. Sincerely, todd the dog (a real dog)")
    print("Said goobye to a member!")


#############################################################################################################
################################################COMMANDS#####################################################
#############################################################################################################

#this decorator will be used for any commands we want to define. The user can call the command by typing 'Todd hi'
@client.command()
async def hi(ctx):
    #await tells us to pause the routine until the message is sent.
    await ctx.send("Hello, I am todd, todd the dog.")
    print("greeted someone!")

#mostenire command
@client.command()
async def mostenire(ctx):
    await ctx.send("mostar")
    print("spelled mostenire correctly!")

#run the bot, linking it to our token. replace this with a string containing your own token.
client.run(DISCORD_TOKEN)