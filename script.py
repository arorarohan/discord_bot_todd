import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from private_config import *
import csv

#define some constants
MOSTENIRE_PATH = 'lists/mostenire_list.csv'
SHAME_PATH = 'lists/file_of_shame.txt'
AUDIO_DIRECTORY = {'whisper':'audio/todd_whispers.mp3'}
TARGETED_USER = ''

#set our intents
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

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


#this next event will detect when squid says literally anything, and store it in a text file
@client.event
async def on_message(message):
    #check if the message was sent by our targeted user
    if message.author.name == TARGETED_USER:
        
        #save the contents in our file
        with open(SHAME_PATH,'a') as file:
            file.write(message.content + '\n')
        
        #say that it has been saved and do the poopoo
        await message.channel.send('poopoo. saved your message in the file of shame. Use <todd file_of_shame> to view.')
        print(f"message {message.content} saved in {SHAME_PATH}")
    
    #without this block, the bot will not do anything with any message if it doesn't execute the above.
    else:
        await client.process_commands(message)

#say something when a member is removed
@client.event
async def on_member_remove(member):

    #once again, first get the channel, then send our message there and tell the host it's been done.
    channel = client.get_channel(WELCOME_CHANNEL)
    await channel.send("Goobye. Guess you weren't a real dog. I shouldn't have called you dog. Sincerely, todd the dog (a real dog)")
    print("Said goobye to a member!")


#############################################################################################################
################################################TEXT COMMANDS################################################
#############################################################################################################

#this decorator will be used for any commands we want to define. The user can call the command by typing 'Todd hi'
@client.command()
async def hi(ctx):
    #await tells us to pause the routine until the message is sent.
    await ctx.send("Hello, I am todd, todd the dog.")
    print("greeted someone!")

#mostenire command to print the list of mostenires from our csv file
@client.command()
async def mostenire_list(ctx):
    message_list = []
    message = ''

    with open(MOSTENIRE_PATH,'r') as file:
        reader = csv.reader(file)
        #add every line in the file to a list
        for line in reader:
            message_list.append(line[0])
        
    #deal with the case that there could be no lines!
    if len(message_list) == 0:
        await ctx.send("There are currently no mostenires in your list.")
        print("returned an empty list of mostenires!")

    else:
        #add every item in the list to a string
        message = "\n".join(message_list)
        #send the string as a message
        await ctx.send(message)
        print("sent a string of mostenires!")


#mostenire add command to add mostenires to the list
@client.command()
async def mostenire_add(ctx,arg=''):
    #don't accept an empty argument
    if not len(arg) > 0:
        await ctx.send("Please try again with an item to add, ex. <todd mostenire_add mositor>")
        print('failed to add to mostenire list as there was nothing to add!')
    else:
        #open the csv
        with open(MOSTENIRE_PATH,'a',newline='') as file:
            writer = csv.writer(file)

            #add the entry
            writer.writerow([arg])
        
        #inform the user and host of our success
        await ctx.send(f"Added {arg} to the list of mostenires! todd thanks you for your service.")
        print(f"added {arg} to {MOSTENIRE_PATH}")


#command to view the file of shame
@client.command()
async def file_of_shame(ctx):
    #get the contents of the file
    with open(SHAME_PATH,'r') as file:
        contents = file.read()
    
    #chuck them out if there's anything to chuck.
    if not contents == '':
        await ctx.send(f"contents of the file of shame (assigned to user {TARGETED_USER}): \n" + contents)
        print("printed the file of shame")
    else:
        await ctx.send(f"the file of shame is assigned to {TARGETED_USER}, but is empty. todd")
        print("called an empty file of shame!")


#command to embed a link to the github repo for this file. shamefully hardcoded, i could bother to scrape the repo for items to populate this embed but i am not bothered.
@client.command()
async def github(ctx):
    
    #define the embed
    embed = discord.Embed(
        title='todd github repo', 
        url='https://github.com/arorarohan/discord_bot_todd', 
        description='Welcome to my GitHub repo for this project! You can find the source code and usage documentation here.',
        color=0x2dba4e
        )
    #include the banner as our awesome thumbnail
    embed.set_image(url='https://github.com/arorarohan/discord_bot_todd/blob/main/assets/banner.png?raw=true')
    #embed.set_image(url='/assets/banner.png')
    #include the author (me)
    embed.set_author(
        name='Rohan A',
        url='https://github.com/arorarohan/',
        icon_url='https://avatars.githubusercontent.com/u/11210289?v=4'
    )
    
    #send the embed
    await ctx.send(embed=embed)
    print("embedded our github repo!")



##################################################################################################################################
#######################################################AUDIO COMMANDS#############################################################
##################################################################################################################################

#join voice channel command
@client.command(pass_context=True)
async def join(ctx):
    #if the user running this command is in a voice channel, join the vc of the user
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        
        #inform the user of our success
        await ctx.send("I am todd. I joined your vc.")
        print("Joined a voice channel and whispered!")
    #if the user is not in a voice channel, tell the user we don't know what channel to join!
    else:
        await ctx.send("Woof. I can see that you aren't in a voice channel. I'm todd and I'm not very smart. I don't know where to go. I'm todd. Join a voice channel and then try again.")
        print("explained why we can't join a voice channel!")


#whisper on-demand, take arg as the item to play
@client.command(pass_context=True)
async def play(ctx,arg=''):
    #first decide what item to play
    if arg in AUDIO_DIRECTORY.keys():
        #play the item
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(AUDIO_DIRECTORY[arg])
        
        #if the bot is not in a vc, we will get an AttributeError
        try:
            player = voice.play(source)
            #inform the user of our success
            await ctx.send(f"played {arg} to you.")
            print(f'played {AUDIO_DIRECTORY[arg]} in a voice channel!')
        except AttributeError:
            await ctx.send("i am todd and I'm not in a vc. Add me to the one you're in first using <todd join>.")

    #we couldn't match the argument to a file
    else:
        #inform the user of our failure
        await ctx.send("Todd can't play what todd don't know. Use <todd play [item to play]>")
        print("failed to play a file as there is nothing to play")


#pause the playback
@client.command(pass_context=True)
async def pause(ctx):
    #call the voice client for the current server of the channel
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)

    #check if we are currently playing audio
    if voice.is_playing():
        voice.pause()
        await ctx.send("todd paused playback. todd is me. i am todd.")
        print("paused playback.")
    else:
        await ctx.send("can't pause if i am not playing anything. i am, however, todd")
        print("failed to pause playback as there is nothing playing.")


#resume playback
@client.command(pass_context=True)
async def resume(ctx):
    #like before, get the voice client for the current server of the current channel.
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)

    #check if we are paused
    if voice.is_paused():
        voice.resume()
        await ctx.send("resumed playback, todd.")
        print("resumed playback.")
    else:
        await ctx.send("todd cannot resume that which does not play in the first place. Woof.")


#command to stop playback
@client.command(pass_context=True)
async def stop(ctx):
    #we don't need to do any checks because there won't be an error if nothing to stop.
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()


#command to leave the vc
@client.command(pass_context=True)
async def leave(ctx):
    #if the bot is already in a voice channel, leave it.
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I am todd. I left the voice channel!")
        print("Left a voice channel!")
    #if the bot is not in a voice channel, we can't leave!
    else:
        await ctx.send("i am todd. I am not in a voice channel. There isn't anything to leave. I'm not very smart but I know this. todd")
        print("explained why we couldn't leave a voice channel!")


#we need a playlist to show the user what files we have and how to call them
@client.command()
async def playlist(ctx):
    #if we don't have anything in the playlist, say so!
    if AUDIO_DIRECTORY == {}:
        await ctx.send("todd think the playlist is empty! Add files to the /audio folder and the audio directory to make them playable woof bark.")
        print("called an empty audio directory!")
    
    #if there are things in the directory, store them in a list of displayable rows
    else:
        message_list = []
        for key, value in AUDIO_DIRECTORY.items():
            message_list.append(f"{key} - {value}")
        
        #make a string to display
        message = "the following items are available to play: use <todd play [keyword on the left]> to play the file on the right. \n"
        message = message + "\n".join(message_list)

        #display the message
        await ctx.send(message)
        print("delivered the playlist for users!")


#run the bot, linking it to our token. replace this with a string containing your own token.
client.run(DISCORD_TOKEN)