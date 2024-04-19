#this file handles events, like when users join and leave, or when the targeted useer says something

from discord.ext import commands
import private_config
import main


class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #for events, this is our decorator now.
    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        #do we have a welcome channel configured?
        if private_config.WELCOME_CHANNEL is not None:
            #get the channel that we want to send our welcome message in
            channel = self.client.get_channel(private_config.WELCOME_CHANNEL)

            #then send our message in that channel, and print that we have done so to the terminal.
            await channel.send("Yo dog, nice to meet you dog. I'm Todd. the dog. woof bark woof.")
            print("Welcomed a new member!")
        
        #if there's no welcome channel, this method will do nothing.
        else:
            pass

    #listen for things in each message
    @commands.Cog.listener()
    async def on_message(self, message):
        #check if the message was sent by our targeted user
        if message.author.name == private_config.TARGETED_USER:
            
            #save the contents in our file
            with open(main.SHAME_PATH,'a') as file:
                file.write(message.content + '\n')
            
            #say that it has been saved and do the poopoo
            await message.channel.send('poopoo. saved your message in the file of shame. Use <todd file_of_shame> to view.')
            print(f"message {message.content} saved in {main.SHAME_PATH}")


    #say goodbye to people who leave.
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        #first check if the welcome channel is configured
        if private_config.WELCOME_CHANNEL is not None:

            #once again, first get the channel, then send our message there and tell the host it's been done.
            channel = self.client.get_channel(private_config.WELCOME_CHANNEL)
            await channel.send("Goobye. Guess you weren't a real dog. I shouldn't have called you dog. Sincerely, todd the dog (a real dog)")
            print("Said goobye to a member!")
        
        #if we don't have a welcome channel
        else:
            pass

#this must be present at the end of every cog file to make it work
async def setup(client):
    await client.add_cog(Greetings(client))