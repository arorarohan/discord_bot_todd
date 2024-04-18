#games you can play with todd! more than just standard-response text commands.

import discord
from discord.ext import commands
import random


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        #first we need our variable outside of the function.
        self.farts = 0

    #game for farting and pooping.

    @commands.command()
    async def fart(self, ctx):

        #if farts < 3 we want to just fart without a chance of pooping.
        if self.farts < 3:
            self.farts += 1
            await ctx.send(f"farted! I have farted {self.farts} times so far. I had 0 chance of pooping just now. woof.")
            print(f"farted. farts = {self.farts}. Poop chance = 0")
        
        #if farts >= 3 we want to have a chance of pooping.
        else:
            #increase poop chance by 10% for each fart over 3.
            poop_chance = 0.2 + 0.1 * (self.farts - 3)
            
            #decide whether to poop
            possibilities = [True, False]
            weights = [poop_chance, 1-poop_chance]
            will_poop = random.choices(possibilities,weights)[0]

            #act accordingly
            if will_poop:
                with open('assets/poop.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)
                await ctx.send(f"I just pooped (had a {poop_chance} chance of doing so). todd say oops.")
                print(f"pooped at {poop_chance}")
                self.farts = 0
            else:
                self.farts += 1
                await ctx.send(f"farted! I have farted {self.farts} times so far. I had a {poop_chance} chance of pooping just now, but i didn't. todd sighs in relief.")
                print(f"farted {self.farts} times at {poop_chance}")


#this must be present at the end of every cog file to make it work
async def setup(client):
    await client.add_cog(Games(client))