#this one is for all the commands that involve interacting with voice channels and playing audio files!

import discord
from discord.ext import commands
import main
from discord import FFmpegPCMAudio

class AudioCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    #join voice channel command
    @commands.command(pass_context=True, brief='joins your call with you. i am with you.')
    async def join(self, ctx):
        #if the user running this command is in a voice channel, join the vc of the user
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            
            #inform the user of our success
            await ctx.send("I am todd. I joined your vc.")
            print("Joined a voice channel!")
        #if the user is not in a voice channel, tell the user we don't know what channel to join!
        else:
            await ctx.send("Woof. I can see that you aren't in a voice channel. I'm todd and I'm not very smart. I don't know where to go. I'm todd. Join a voice channel and then try again.")
            print("explained why we can't join a voice channel!")    

    #play sound file on-demand, take arg as the item to play
    @commands.command(pass_context=True, brief='play some music! Use <todd play [filename]>')
    async def play(self, ctx,arg=''):
        #initialize our voice
        voice = ctx.guild.voice_client
        
        #check if the item to play exists
        if arg in main.AUDIO_DIRECTORY.keys():
            #then check if anything is playing
            if voice.is_playing():
                await ctx.send("could not play that, as todd is already in the middle of a pawsome performance!")
                print("failed to play as something is already playing")
            #if nothing is playing, we move on
            else:
            #play the item
                source = FFmpegPCMAudio(main.AUDIO_DIRECTORY[arg])
                
                #if the bot is not in a vc, we will get an AttributeError
                try:
                    player = voice.play(source)
                    #inform the user of our success
                    await ctx.send(f"played {arg} to you.")
                    print(f'played {main.AUDIO_DIRECTORY[arg]} in a voice channel!')
                except AttributeError:
                    await ctx.send("i am todd and I'm not in a vc. Add me to the one you're in first using <todd join>.")

        #we couldn't match the argument to a file
        else:
            #inform the user of our failure
            await ctx.send("Todd can't play what todd don't know. Use <todd play [item to play]>")
            print("failed to play a file as there is nothing to play")
    
    #pause the playback
    @commands.command(pass_context=True, brief='pauses the music. todd is sad.')
    async def pause(self, ctx):
        #call the voice client for the current server of the channel
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)

        #check if we are currently playing audio
        if voice.is_playing():
            voice.pause()
            await ctx.send("todd paused playback. todd is me. i am todd.")
            print("paused playback.")
        else:
            await ctx.send("can't pause if i am not playing anything. i am, however, todd")
            print("failed to pause playback as there is nothing playing.")
    
    #resume playback
    @commands.command(pass_context=True, brief='resumes to music. todd')
    async def resume(self, ctx):
        #like before, get the voice client for the current server of the current channel.
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)

        #check if we are paused
        if voice.is_paused():
            voice.resume()
            await ctx.send("resumed playback, todd.")
            print("resumed playback.")
        else:
            await ctx.send("todd cannot resume that which does not play in the first place. Woof.")
    

    #command to stop playback
    @commands.command(pass_context=True, brief='todd stop the music. sorry')
    async def stop(self, ctx):
        #we don't need to do any checks because there won't be an error if nothing to stop.
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
        voice.stop()

    
    #command to leave the vc
    @commands.command(pass_context=True, brief='DO NOT WRITE THIS COMAND. YOU WANT ME HERE.')
    async def leave(self, ctx):
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
    @commands.command(brief='shows all songs todd can sing')
    async def playlist(self, ctx):
        #if we don't have anything in the playlist, say so!
        if main.AUDIO_DIRECTORY == {}:
            await ctx.send("todd think the playlist is empty! Add files to the /audio folder and the audio directory to make them playable woof bark.")
            print("called an empty audio directory!")
        
        #if there are things in the directory, store them in a list of displayable rows
        else:
            message_list = []
            for key, value in main.AUDIO_DIRECTORY.items():
                message_list.append(f"{key} - {value}")
            
            #make a string to display
            message = "the following items are available to play: use <todd play [keyword on the left]> to play the file on the right. \n"
            message = message + "\n".join(message_list)

            #display the message
            await ctx.send(message)
            print("delivered the playlist for users!")

#this must be present at the end of every cog file to make it work
async def setup(client):
    await client.add_cog(AudioCommands(client))