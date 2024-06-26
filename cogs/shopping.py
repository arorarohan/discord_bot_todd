# for all shopping and item-related commands!
import discord
from discord.ext import commands
import main
from scripts import helpers
import csv
from scripts.dictionaries import Dictionaries

class Shopping(commands.Cog):
    def __init__(self, client):
        self.client = client

        #bring in our shop items from the dictionaries file
        dictionaries = Dictionaries()
        dictionaries.load_shop_items()
        self.shop_items = dictionaries.shop_items

    #view the shop
    @commands.command(brief='spend money get pretty. see how you can spend your toddallions')
    async def shop(self,ctx):

        #get all the shop items as lines in a list
        lines = []
        for key, value in self.shop_items.items():
            lines.append(f"{key} --- {value['value']}")
        
        #print our message, including all the lines in the list separated by newlines.
        message = "Below are the items currently available in the shop! Prices listed in Toddallions. Use <todd buy [item_name]> to buy! (all purchases are non-refundable, non-exchangable and have no warranty) \n\n" + "\n".join(lines) + "\n\nNot enough toddallions? Play games to earn more! Use <todd help> to see avaiable games."
        await ctx.send(message)
        print('displayed the shop!')


    # check balance
    @commands.command(brief='u rich or u poor? now u can see')
    async def balance(self, ctx):
        bal = helpers.check_balance(ctx.author.name)
        await ctx.send(f"your balance is {bal} toddallions!")
        print(f'returned {ctx.author.name}\'s balance as {bal} toddallions!')


    #buy items
    @commands.command(brief='get stuff! toddsumerism. use <todd buy [item from shop]>')
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
            price = self.shop_items[arg]['value']
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
    @commands.command(brief='what do you have? can todd have some?')
    async def inventory(self,ctx):
        #use the function we made in helpers.py to fetch a list of items this user owns!
        items_list = helpers.get_inventory_list(ctx.author.name)

        #add these items to a message and send it
        message = "your inventory contains: \n\n" + "\n".join(items_list) + "\n\nUse your items with <todd use [item]>. Want more items? Buy them in the shop with <todd shop>!"
        await ctx.send(message)
        print(f'displayed inventory of {ctx.author.name}!')
    
    #command to view the net worth leaderboard
    @commands.command(brief='view the most wealthy members of the todd family!')
    async def leaderboard(self,ctx):
        #get everything from the csv in a list
        with open(main.TODDALLIONS_PATH,'r') as file:
            items = list(csv.reader(file))

        #now let's factor in net worth for each user by checking inventory!
        net_worth_list = []
        for i in range(len(items)):
            #get the list of items owned by the user
            username = items[i][0]
            owned_items = helpers.get_inventory_list(username)
            
            #get the sum of values of these items
            assets_value = 0
            #only bother to sum assets value if there are any assets to sum.
            if not owned_items == []:
                for item in owned_items:
                    item_value = self.shop_items[item]['value']
                    assets_value += item_value
        
            #calculate net worth
            net_worth = int(items[i][1]) + assets_value
            
            #add it to the list
            net_worth_list.append([username, net_worth])
        
        #once we have our full list, let's sort it before we display
        sorted_list = helpers.sort_toddalions(net_worth_list)
        
        #time to construct our output message
        #make a list of strings to print: each line is a string with an index number (starting from 1) followed by the username, followed by the number of coins!
        lines = [f'{i+1}. {sorted_list[i][0]} --- {sorted_list[i][1]} toddallions' for i in range(len(sorted_list))]
        
        #make a message string to display and send it
        message = "Net worth leaderboard (inclusive of toddallions and purchased items): \n\n" + "\n".join(lines) + "\n\nTo climb, grind toddallions by playing games! Use <todd help> to see available games."
        await ctx.send(message)
        print('delivered the leaderboard!')

    
    #command to use an item in your inventory
    @commands.command(brief='use an item from your inventory! use <todd use [item]>')
    async def use(self, ctx, item_to_use):
        
        #first we validate that this is in the user's inventory
        inv_list = helpers.get_inventory_list(ctx.author.name)
        #abort with a message if we didn't find that item
        if item_to_use not in inv_list:
            await ctx.send('Can\'t use that item, because it isn\'t in your inventory!')
            print(f'use failed: could not find {item_to_use} in {inv_list}')
            return
        
        #now validate that the item was something bought from the shop, otherwise we have no data on it.
        if item_to_use not in self.shop_items.keys():
            await ctx.send('Can\'t use that item, because it isn\'t an official shop item!')
            print(f'use failed: could not find {item_to_use} in {self.shop_items.keys()}')
            return
        
        #if we're here, the item can be used. So let's use it! This means we will send out the message and image associated with the item
        #first we fetch and send the image, if there is an image
        item_image = self.shop_items[item_to_use]['image']
        if item_image is not None:
            with open(item_image,'rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)

        #then we send a message.
        
        #immortality is the special case. it's too long so we broke it up into 3 messages.
        if item_to_use == 'immortality':
            await ctx.send(self.shop_items[item_to_use]['message1'])
            await ctx.send(self.shop_items[item_to_use]['message2'])
            await ctx.send(self.shop_items[item_to_use]['message3'])

        #for the normal case, we only need to send 1 message.
        else:
            await ctx.send(self.shop_items[item_to_use]['message'])
            
        #finally, we print to the console and return
        print(f'{ctx.author.name} used {item_to_use}!')
        return  
        



#this must be present at the end of every cog file to make it work. don't ask me why. it's just how it is. like how the sky is blue (when there isn't a storm, and it's daytime) and how the sky is not blue otherwise.
async def setup(client):
    await client.add_cog(Shopping(client))