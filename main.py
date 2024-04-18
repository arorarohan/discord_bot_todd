#this is the file to run, to activate the bot!

import discord
from discord.ext import commands
import private_config
import asyncio

#define some constants
MOSTENIRE_PATH = 'lists/mostenire_list.csv'
SHAME_PATH = 'lists/file_of_shame.txt'

AUDIO_DIRECTORY = {
    'whisper':'audio/todd_whispers.mp3',
    'chandelier':'audio/todd_sings_chandelier.mp3',
    }


def run():
    #set our intents
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True

    #initialize the client, set the prefix for bot commands to be 'todd '.
    client = commands.Bot(command_prefix='todd ', intents=intents)

    #once the bot has connected, set it up and let the host know it's ready
    @client.event
    async def on_ready():
        #load all our cogs
        await client.load_extension('cogs.events')
        await client.load_extension('cogs.error_handling')
        await client.load_extension('cogs.text_commands')
        await client.load_extension('cogs.audio_commands')

        #set todd's status
        await client.change_presence(activity=discord.CustomActivity('sniffing around, being todd.'))

        #this is printed to the terminal for the host, not visible to the user
        print("The bot is now ready for use!")
        print("------------------------------------")

    
    client.run(private_config.DISCORD_TOKEN)


#actually run the bot!
if __name__ == '__main__':
    asyncio.run(run())