#this file handles generic error handling, to make sure there is some feedback if the error isn't handled by the function of the specific command used.

from discord.ext import commands


class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    #error handling messages, catch-all non-specific errors so that in the worst case that our error has not been handled by the specific function, we at least can give some generic feedback.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        #missing perms
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to run this command!")
            print("ERROR: user didn't have the perms")
        #can't read the channel
        if isinstance(error, commands.ChannelNotReadable):
            await ctx.send("I can't read this channel, fix my perms!")
            print("ERROR: couldn't read the channel")
        #unkown command
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("todd doesn't know that command yet!! use <todd help> for a list of commands")
            print("ERROR: received an unknown command")
        #member not found
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("todd sniffed through the entire server and couldn't find that member!")
            print("ERROR: member not found")
        #missing argument
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("you were supposed to give todd an argument, but you didn't , oh no, todd whimpers")
            print("ERROR: missing required argument")
        #invalid argument type
        if isinstance(error, commands.BadArgument):
            await ctx.send('invalid argument type! If you entered a user, make sure they\'ve been pinged. todd cries.')


#this must be present at the end of every cog file to make it work
async def setup(client):
    await client.add_cog(ErrorHandling(client))