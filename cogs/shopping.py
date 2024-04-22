# for all shopping-related commands!
import discord
from discord.ext import commands
import main
import helpers

class Shopping(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.shop_items = {
            'collar':50,
            'pickle':20,
            'squeaky_toy':100,
            'golden_statue':500,
            'dog_training_book':150,
            'stuffed_panda':200
        }

    #view the shop
    @commands.command()
    async def shop(self,ctx):

        #get all the shop items as lines in a list
        lines = []
        for key, value in self.shop_items.items():
            lines.append(f"{key} --- {value}")
        
        #print our message, including all the lines in the list separated by newlines.
        message = "Below are the items currently available in the shop! Prices listed in Toddallions. Use <todd buy [item_name]> to buy! (all purchases are non-refundable, non-exchangable and have no warranty) \n\n" + "\n".join(lines) + "\n\nNot enough toddallions? Play fetch to earn more!"
        await ctx.send(message)
        print('displayed the shop!')


    # check balance
    @commands.command()
    async def balance(self, ctx):
        bal = helpers.check_balance(ctx.author.name)
        await ctx.send(f"your balance is {bal} toddallions!")
        print(f'returned {ctx.author.name}\'s balance as {bal} toddallions!')


    #buy items
    @commands.command()
    async def buy(self,ctx,arg=''):
        #don't accept an empty argument.
        if arg == '':
            await ctx.send('Buy what? Use <todd buy [item]>. Not sure what\'s available? Use <todd shop>!')
            print('failed to buy: no argument!')
        #also don't accept an item that is not even in the catalog.
        elif arg not in self.shop_items.keys():
            await ctx.send(f'item {arg} isn\'t in the shop! Use <todd shop> to see available items.')
            print('failed to buy: invalid argument!')
        
        #with a valid argument, we proceed to get the price and make the required changes.
        else:
            price = self.shop_items[arg]
            available_balance = helpers.check_balance(ctx.author.name)
            
            #determine whether the user can afford it
            if price <= available_balance:
                #buy it by updating the user's balance and delivering the item
                helpers.update_balance(ctx.author.name, -price)
                helpers.add_to_inventory(ctx.author.name, arg)
                await ctx.send(f'congratulations, you bought {arg}! Remaining balance: {helpers.check_balance(ctx.author.name)}')
                print(f'{ctx.author.name} just bought {arg} for {price}!')
            
            #if the user can't afford it
            else:
                await ctx.send(f'you can\'t afford that item! It costs {price} but you only have {available_balance}')
                print(f'{ctx.author.name} failed to purchase {arg}: {available_balance} < {price}')


    #check inventory
    @commands.command()
    async def inventory(self,ctx):
        #use the function we made in helpers.py to fetch a list of items this user owns!
        items_list = helpers.get_inventory_list(ctx.author.name)

        #add these items to a message and send it
        message = "your inventory contains: \n\n" + "\n".join(items_list) + "\n\nWant more items? Buy them in the shop with <todd shop>!"
        await ctx.send(message)
        print(f'displayed inventory of {ctx.author.name}!')


#this must be present at the end of every cog file to make it work. don't ask me why. it's just how it is. like how the sky is blue (when there isn't a storm, and it's daytime) and how the sky is not blue otherwise.
async def setup(client):
    await client.add_cog(Shopping(client))