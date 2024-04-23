#this file is for our custom help command implementation

from typing import Any
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):

    #inherit the constructor from the parent class
    def __init__(self):
        super().__init__()

    #this will take effect when the user sends <todd help> - it is the overall help command for the bot
    async def send_bot_help(self, mapping):
        #we use get_destination to get ctx
        print('recognized the help command')
        ctx = self.get_destination()

        #for each cog, let's save the list of commands under it to the message
        message_list = list()
        for cog in mapping:

            #there can be None objects in the mapping for some reason. We need to exclude them so they don't break the rest of the loop.
            if cog == None:
                continue
            else:
                #first let's get the names and descriptions
                command_names = [command.name for command in mapping[cog]]
                command_descs = [command.brief for command in mapping[cog]]
                
                #if there are commands, we proceed, else we skip this cog because it isn't one that houses commands.
                if len(command_names) == 0:
                    continue
                else:
                    message_list.append(f'\n**{cog.qualified_name}**\n')
                    for i in range(len(command_names)):
                        message_list.append(f'**{command_names[i]}** --- {command_descs[i]}\n')
        
        #once done, send the message
        await ctx.send("".join(message_list))
        print('sent the help list!')
        return
            
    
    #we are turning off all the below commands because we don't want them. To do so, we will just pretend todd didn't recognize that command at all.
    #this will take effect when the user sends <todd help Cog> for example <todd help Games> - it is the help command for specific cogs.
    async def send_cog_help(self, cog):
        ctx = self.get_destination()
        await ctx.send("todd doesn't know that command yet!! use <todd help> for a list of commands")
        print("ERROR: received an unknown command")
        return
    
    #we aren't using groups so we don't care about this feature
    async def send_group_help(self, group):
        ctx = self.get_destination()
        await ctx.send("todd doesn't know that command yet!! use <todd help> for a list of commands")
        print("ERROR: received an unknown command")
        return
    
    #this will take effect when the user sends <todd help command> for example <todd help fetch> - it gives help for specific commands. Not sure if we want to implement this yet.
    async def send_command_help(self, command):
        ctx = self.get_destination()
        await ctx.send("todd doesn't know that command yet!! use <todd help> for a list of commands")
        print("ERROR: received an unknown command")
        return