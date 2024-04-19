#this one is for all our standard-response text-based commands (non-AI)

import private_config
import discord
from discord.ext import commands
import main
import csv

class TextCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #hi!
    @commands.command()
    async def hi(self, ctx):
        #await tells us to pause the routine until the message is sent.
        await ctx.send("Hello, I am todd, todd the dog.")
        print("greeted someone!")

    #mostenire command to print the list of mostenires from our csv file
    @commands.command()
    async def mostenire_list(self, ctx):
        message_list = []
        message = ''

        with open(main.MOSTENIRE_PATH,'r') as file:
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
    @commands.command()
    async def mostenire_add(self, ctx, arg=''):
        #don't accept an empty argument
        if not len(arg) > 0:
            await ctx.send("Please try again with an item to add, ex. <todd mostenire_add mositor>")
            print('failed to add to mostenire list as there was nothing to add!')
        else:
            #open the csv
            with open(main.MOSTENIRE_PATH,'a',newline='') as file:
                writer = csv.writer(file)

                #add the entry
                writer.writerow([arg])
            
            #inform the user and host of our success
            await ctx.send(f"Added {arg} to the list of mostenires! todd thanks you for your service.")
            print(f"added {arg} to {main.MOSTENIRE_PATH}")

    #command to view the file of shame
    @commands.command()
    async def file_of_shame(self, ctx):
        #don't run if there isn't an assigned user
        if private_config.TARGETED_USER == '':
            await ctx.send("no user assigned to the file of shame!")
            print("file of shame asked for, but no user assigned!")
        else:
            #get the contents of the file
            with open(main.SHAME_PATH,'r') as file:
                contents = file.read()
            
            #chuck them out if there's anything to chuck.
            if not contents == '':
                await ctx.send(f"contents of the file of shame (assigned to user {private_config.TARGETED_USER}): \n" + contents)
                print("printed the file of shame")
            else:
                await ctx.send(f"the file of shame is assigned to {private_config.TARGETED_USER}, but is empty. todd")
                print("called an empty file of shame!")
    

    #command to embed a link to the github repo for this file. shamefully hardcoded, i could bother to scrape the repo for items to populate this embed but i am not bothered.
    @commands.command()
    async def github(self, ctx):
        
        #define the embed
        embed = discord.Embed(
            title='todd github repo', 
            url='https://github.com/arorarohan/discord_bot_todd', 
            description='Welcome to my GitHub repo for this project! You can find the source code and usage documentation here.',
            color=0x2dba4e
            )
        #include the banner as our awesome thumbnail
        embed.set_image(url='https://github.com/arorarohan/discord_bot_todd/blob/main/assets/banner.png?raw=true')
        #embed.set_image(url='/assets/banner.png') is what i wanted to do but it didn't work
        #include the author (me)
        embed.set_author(
            name='Rohan A',
            url='https://github.com/arorarohan/',
            icon_url='https://avatars.githubusercontent.com/u/11210289?v=4'
        )
        
        #send the embed
        await ctx.send(embed=embed)
        print("embedded our github repo!")


    #command to view the hall of fame!
    @commands.command()
    async def hall_of_fame(self, ctx):
        #get the contents of our hall of fame
        with open(main.FAME_PATH,'r') as file:
            items = list(csv.reader(file))
        
        #don't bother doing anything if there's nothing there
        if len(items) == 0:
            await ctx.send("the hall of fame is currently empty! This will activate once users start discovering gold. use <todd fetch> to play!")
            print("tried to deliver the hall of fame, but it was empty!")
        
        else:
            #split it into users and scores
            message = []
            for item in items:
                message.append(f"{item[0]} --- {item[1]} ingots!")
            
            #make our message a string
            message_str = "The hall of fame is a special place for a special few users who find gold! The list of inductees (unsorted because todd isn't smart enough to sort it) is:\n\n" + "\n".join(message) + "\n\n to become one of them, play <todd fetch>. Happy hunting!"

            #send it
            await ctx.send(message_str)
            print("delivered the hall of fame!")

        

#this must be present at the end of every cog file to make it work
async def setup(client):
    await client.add_cog(TextCommands(client))