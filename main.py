#this is the file to run, to activate the bot!

import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

#import sensitive constants from dotenv file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CHANNEL = os.getenv('WELCOME_CHANNEL')
TARGETED_USER = os.getenv('TARGETED_USER')

#define some constants
MOSTENIRE_PATH = 'lists/mostenire_list.csv'
SHAME_PATH = 'lists/file_of_shame.txt'
FAME_PATH = 'lists/hall_of_fame.csv'
INVENTORY_PATH = 'lists/inventory.csv'
TODDALLIONS_PATH = 'lists/toddallions.csv'

AUDIO_DIRECTORY = {
    'whisper':'audio/todd_whispers.mp3',
    'chandelier':'audio/todd_sings_chandelier.mp3',
    }


def run():
    #create required files if they don't exist
    print('creating required files if needed...')
    if not os.path.exists(FAME_PATH):
        with open(FAME_PATH,'w',newline='') as file:
            file.close()
        print(f'created {FAME_PATH}')
    if not os.path.exists(SHAME_PATH):
        with open(SHAME_PATH,'w') as file:
            file.close()
        print(f'created {SHAME_PATH}')
    if not os.path.exists(MOSTENIRE_PATH):
        with open(MOSTENIRE_PATH,'w') as file:
            file.close()
        print(f'created {MOSTENIRE_PATH}')
    if not os.path.exists(INVENTORY_PATH):
        with open(INVENTORY_PATH,'w') as file:
            file.close()
        print(f'created {INVENTORY_PATH}')
    if not os.path.exists(TODDALLIONS_PATH):
        with open(TODDALLIONS_PATH,'w') as file:
            file.close()
        print(f'created {TODDALLIONS_PATH}')
    print('required files created!')



    #set our intents
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True

    #initialize the client, set the prefix for bot commands to be 'todd '.
    client = commands.Bot(command_prefix=['todd ', 'Todd '], intents=intents)

    #once the bot has connected, set it up and let the host know it's ready
    @client.event
    async def on_ready():
        #load all our cogs
        print('loading cogs...')
        await client.load_extension('cogs.events')
        await client.load_extension('cogs.error_handling')
        await client.load_extension('cogs.text_commands')
        await client.load_extension('cogs.audio_commands')
        await client.load_extension('cogs.games')
        await client.load_extension('cogs.shopping')
        print('cogs loaded!')

        #set todd's status
        await client.change_presence(activity=discord.CustomActivity('sniffing around, being todd.'))
        print('status set!')

        #this is printed to the terminal for the host, not visible to the user
        print("The bot is now ready for use!")
        print("------------------------------------")

    print('starting client...')
    client.run(DISCORD_TOKEN)


#actually run the bot!
if __name__ == '__main__':
    asyncio.run(run())