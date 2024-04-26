#for trading-related commands!
import discord
from discord.ext import commands
from scripts import helpers, trade_request

class Trading(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.open_trade_requests: list[trade_request.TradeRequest] = list() #this will be a list of objects of type TradeRequest

    #initiate a trade request with another user
    @commands.command(brief='send a trade request to another user! Use <todd trade @user> to start')
    async def trade(self,ctx, target_user: discord.User):
        
        #get the usernames we will be using
        sender_username = ctx.author.name
        recipient_username = target_user.name

        #first check if we received a valid argument.
        #can't trade with yourself.
        if sender_username == recipient_username:
            await ctx.send('you can\'t trade with yourself, that isn\'t how this works. even todd knows this. and he\'s a dog.')
            print('trade failed: cannot trade with self.')
            return
        
        #can't trade with someone who is not in this server: we could remove this restriction later but for now let's keep it.
        #get a list of the mutual servers of todd and the recipient. We will compare it to the name of this server
        mutuals = target_user.mutual_guilds
        this_server = ctx.message.guild #the server the trade command was called in
        
        #we will search through every server in the mutuals list and compare its name to the name of the server the command was triggered from.
        in_server = False
        #don't bother searching if there are no mutual servers (this would happen if todo has been removed from the server the target user used to be in)
        if mutuals != []:
            #conduct the search and set in_server to True if we found this server in the list
            for server in mutuals:
                if server.name == this_server.name:
                    in_server = True
                    break
        
        #if the recipient isn't in this server, we terminate.
        if not in_server:
            await ctx.send('you can\'t trade with that user as they aren\'t in this server! either invite them (todd wants everyone to be together) or trade with someone else!')
            print('trade failed: victim not in server')
            return

        #now we need to display inventories to the user so they can make a choice.
        #first get a list of inventory items for the sender
        inv_sender_list = helpers.get_inventory_list(sender_username)
        inv_sender_str = "\n".join(inv_sender_list)

        #then do the same for the recipient
        inv_recipient_list = helpers.get_inventory_list(recipient_username)
        inv_recipient_str = "\n".join(inv_recipient_list)

        #if either person has nothing in their inventory, we can't do the trade
        if inv_sender_list == []:
            await ctx.send('You can\'t trade as your inventory is empty!')
            print('trade failed: sender inventory is empty')
            return
        if inv_recipient_list == []:
            await ctx.send('You can\'t trade as your trading partner\'s inventory is empty!')
            print('trade failed: recipient inventory is empty')
            return

        #now that a trade is possible, we initialize our trade request.
        request = trade_request.TradeRequest(sender_username, recipient_username)

        #now combine them into a message and send it, prompting the user for their item
        message = f"Your inventory: \n{inv_sender_str}\n\n{recipient_username}\'s inventory: \n{inv_recipient_str}\n\nFirst type the name of the item from your inventory to trade:"
        await ctx.send(message)

        #checking function to vet selection messages, so that only the sender can confirm.
        def check(m):
            return ctx.author.name == m.author.name

        #get the selection from the user
        sender_selection_msg = await self.client.wait_for('message', check=check)
        #extract the content of the message object
        sender_selection = sender_selection_msg.content

        #attempt to set the item, track its success in a variable selected (the method has a True/False output)
        selected = request.set_sender_item(sender_selection)
        
        #in case it didn't go through, request again until it does.
        if not selected:
            while not selected:
            #use a while loop to keep checking until we get a valid selection
                await ctx.send('invalid selection, enter the name of the item from your inventory, exactly as it appears in the list.')

                #get a new selection, and get the content of that message object, then attempt to set
                sender_selection_msg = await self.client.wait_for('message', check=check)
                sender_selection = sender_selection_msg.content
                selected = request.set_sender_item(sender_selection)
    
        #now that we have something selected, repeat the process for the recipient's inventory.
        message = f"Now type the name of the item from {recipient_username}\'s inventory to trade:"
        await ctx.send(message)
        
        #get the selection from the user
        recipient_selection_msg = await self.client.wait_for('message', check=check)
        #extract the content of the message object
        recipient_selection = recipient_selection_msg.content

        #attempt to set the item, track its success in a variable selected (the method has a True/False output)
        selected = request.set_recipient_item(recipient_selection)
        
        #in case it didn't go through, request again until it does.
        if not selected:
            while not selected:
            #use a while loop to keep checking until we get a valid selection
                await ctx.send(f'invalid selection, enter the name of the item from {recipient_username}\'s inventory, exactly as it appears in the list.')

                #get a new selection, and get the content of that message object, then attempt to set.
                recipient_selection_msg = await self.client.wait_for('message', check=check)
                recipient_selection = recipient_selection_msg.content
                selected = request.set_recipient_item(recipient_selection)

        #now we have the essential information of the trade request, let's confirm before storing it

        await ctx.send(f'You want to trade your {request.sender_item} with {request.recipient_username}\'s {request.recipient_item}, are you sure? (y/n)')
        confirmation_message = await self.client.wait_for('message', check=check)
        
        #check the decision
        try:
            decision = helpers.get_confirmation(confirmation_message.content)
        
        #if there was an exception it means the confirmation message wasn't valid (y/n).
        except Exception:
            #so we need to keep prompting until we don't get an exception
            while True:
                await ctx.send('invalid decision, enter y to proceed with the trade and n to cancel it.')
                print('invalid decision received, getting new decision')
                confirmation_message = await self.client.wait_for('message', check=check)

                #check this decision again and break if we don't get an exception. Until that happens we'll just keep looping.
                try:
                    decision = helpers.get_confirmation(confirmation_message.content)
                    break
                except Exception:
                    continue
        
        #now abort if the confirmation is negative
        if decision == False:
            await ctx.send('aborted transaction')
            print('trade failed: aborted by user')
            return
        
        #if we made it here, they said yes! so let's add the trade request object to the list of open requests.
        self.open_trade_requests.append(request)
        await ctx.send('trade request sent!')
        return

    #view trade requests
    @commands.command(brief='view your incoming and outgoing trade requests!')
    async def trade_requests(self,ctx):
        username = ctx.author.name
        #first we make a list of all the user's incoming requests.
        incoming_requests: list[trade_request.TradeRequest] = []
        
        #loop through the lis (only if it isn't empty) and copy any object addressed to the user to incoming_requests
        if self.open_trade_requests != []:
            for request in self.open_trade_requests:
                if request.recipient_username == username:
                    incoming_requests.append(request)

        #now that we have their incoming requests, add them to the message, including an index. Otherwise, tell the user that there isn't anything.
        if incoming_requests != []:
            incoming_message_li = [f'{idx + 1}. {incoming_requests[idx].get_preview()}' for idx in range(len(incoming_requests))]
            #turn this into a string
            incoming_message = "\n".join(incoming_message_li)
        else:
            #the other case is that there are no incoming requests
            incoming_message = 'You have no incoming trade requests!'
        
        #now do the same for outgoing requests
        outgoing_requests: list[trade_request.TradeRequest] = []
        
        #loop through the lis (only if it isn't empty) and copy any object addressed to the user to outgoing_requests
        if self.open_trade_requests != []:
            for request in self.open_trade_requests:
                if request.sender_username == username:
                    outgoing_requests.append(request)

        #now that we have their outgoing requests, add them to the message, including an index. Otherwise, tell the user that there isn't anything.
        if outgoing_requests != []:
            outgoing_message_li = [f'{idx + 1}. {outgoing_requests[idx].recipient_username}: trade your {outgoing_requests[idx].sender_item} for their {outgoing_requests[idx].recipient_item}' for idx in range(len(outgoing_requests))]
            #turn this into a string
            outgoing_message = "\n".join(outgoing_message_li)
        else:
            #the other case is that there are no outgoing requests
            outgoing_message = 'You have no outgoing trade requests!'
        
        #now we format and send our message
        await ctx.send(f"Your incoming trade requests are: \n\n{incoming_message}\n\nYour outgoing trade requests are: \n\n{outgoing_message}\n\nTo accept incoming requests, enter accept mode with <todd trade_accept>. To decline incoming requests, use <todd trade_decline>.")
        print('delivered list of trade requests!')
        return

    #accept trade requests
    @commands.command(brief='view and accept trade requests!')
    async def trade_accept(self,ctx):
        
        #first we copy over everything from self.trade_requests as we want to display them like before.
        #first we make a list of all the user's incoming requests.
        incoming_requests: list[trade_request.TradeRequest] = []
        username = ctx.author.name
        
        #loop through the lis (only if it isn't empty) and copy any object addressed to the user to incoming_requests
        if self.open_trade_requests != []:
            for request in self.open_trade_requests:
                if request.recipient_username == username:
                    incoming_requests.append(request)

        #now that we have their incoming requests, add them to the message, including an index. Otherwise, tell the user that there isn't anything and return as we have nothing left to do.
        if incoming_requests != []:
            message_li = [f'{idx + 1}. {incoming_requests[idx].get_preview()}' for idx in range(len(incoming_requests))]
            #turn this into a string
            message = "\n".join(message_li)
            await ctx.send(f'Your incoming trade requests are: \n\n{message}\n\nType the index number of the request you want to accept! Type anything else to abort.')
        
        else:
            await ctx.send('You have no incoming trade requests to accept!')
            #in this case, we return as we don't want to continue in this case.
            return
        
        #define a checking function to screen responses
        def check(m):
            return ctx.author.name == m.author.name
        
        #wait for a response from the user
        selection_message = await self.client.wait_for('message', check=check)
        selection = selection_message.content

        #make sure they chose an integer, if they didn't, abort
        try:
            selection = int(selection)
        except ValueError:
            await ctx.send('invalid response! aborted.')
            print('trade acceptance failed: invalid selection')
            return
        
        #make sure the integer they chose was within the range of possible choices.
        if selection > len(incoming_requests):
            await ctx.send('invalid response, the number you chose was outside the range of the list. aborted.')
            print('trade acceptance failed: selection out of range')
            return
        
        #if we're here then the choice was valid. So ask the user if the are sure.
        selected_request = incoming_requests[selection-1]
        await ctx.send(f'are you sure you want to accept this trade? you will receive {selected_request.sender_item}, and will give {selected_request.sender_username} your {selected_request.recipient_item}. (y/n)')
        
        #get the decision from the user
        decision_msg = await self.client.wait_for('message', check=check)
        
        #check the decision
        try:
            decision = helpers.get_confirmation(decision_msg.content)
        
        #if there was an exception it means the confirmation message wasn't valid (y/n).
        except Exception:
            #so we need to keep prompting until we don't get an exception
            while True:
                await ctx.send('invalid decision, enter y to accept the trade and n to cancel.')
                print('invalid decision received, getting new decision')
                decision_msg = await self.client.wait_for('message', check=check)

                #check this decision again and break if we don't get an exception. Until that happens we'll just keep looping.
                try:
                    decision = helpers.get_confirmation(decision_msg.content)
                    break
                except Exception:
                    continue

        #cancel if the user said no.
        if decision == False:
            await ctx.send('trade cancelled.')
            print('trade cancelled by user')
            return
        
        #if we made it here, they said yes! but before we can process the trade, check that the users still have the items they are trading!
        sender_list = helpers.get_inventory_list(selected_request.sender_username)
        if selected_request.sender_item not in sender_list:
            await ctx.send(f'transaction failed, {selected_request.sender_username} no longer has the item they were offering to give you!')
            print('trade acceptance failed: sender no longer has offered item')
            return
        
        recipient_list = helpers.get_inventory_list(selected_request.recipient_username)
        if selected_request.recipient_item not in recipient_list:
            await ctx.send(f'transaction failed, you no longer have the item {selected_request.sender_username} wants from you!')
            print('trade acceptance failed: recipient no longer has requested item')
            return
        
        #if we made it here, we can actually fulfil the request
        selected_request.fulfil_request()

        #now find the request in the list and delete it.
        for i in range(len(self.open_trade_requests)):
            if self.open_trade_requests[i] == selected_request:
                self.open_trade_requests.pop(i)
                print('request deleted!')
                break
        
        await ctx.send('trade completed!')
        print(f'trade successful: {selected_request.sender_username} traded their {selected_request.sender_item} with {selected_request.recipient_username}\'s {selected_request.recipient_item}!')
        return


    #decline trade requests
    @commands.command(brief='view and decline trade requests!')
    async def trade_decline(self,ctx):
        #first we make a list of all the user's incoming requests.
        incoming_requests: list[trade_request.TradeRequest] = []
        username = ctx.author.name
        
        #loop through the list (only if it isn't empty) and copy any object addressed to the user to incoming_requests
        if self.open_trade_requests != []:
            for request in self.open_trade_requests:
                if request.recipient_username == username:
                    incoming_requests.append(request)

        #now that we have their incoming requests, add them to the message, including an index. Otherwise, tell the user that there isn't anything and return as we have nothing left to do.
        if incoming_requests != []:
            message_li = [f'{idx + 1}. {incoming_requests[idx].get_preview()}' for idx in range(len(incoming_requests))]
            #turn this into a string
            message = "\n".join(message_li)
            await ctx.send(f'Your incoming trade requests are: \n\n{message}\n\nType the index number of the request you want to decline! Type anything else to abort.')
        
        else:
            await ctx.send('You have no incoming trade requests to decline!')
            #in this case, we return as we don't want to continue in this case.
            return
        
        #define a checking function to screen responses
        def check(m):
            return ctx.author.name == m.author.name
        
        #wait for a response from the user
        selection_message = await self.client.wait_for('message', check=check)
        selection = selection_message.content

        #make sure they chose an integer, if they didn't, abort
        try:
            selection = int(selection)
        except ValueError:
            await ctx.send('invalid response! aborted.')
            print('trade decline failed: invalid selection')
            return
        
        #make sure the integer they chose was within the range of possible choices.
        if selection > len(incoming_requests):
            await ctx.send('invalid response, the number you chose was outside the range of the list. aborted.')
            print('trade decline failed: selection out of range')
            return
        
        #if we're here then the choice was valid. So we select the request accordingly and ask the user if they are sure.
        selected_request = incoming_requests[selection-1] #offset by 1 because our list indices start from 0 but they are presented to the user starting from 1
        await ctx.send(f'are you sure you want to decline this trade? {selected_request.get_preview()}. (y/n)')
        
        #get the decision from the user
        decision_msg = await self.client.wait_for('message', check=check)
        
        #check the decision
        try:
            decision = helpers.get_confirmation(decision_msg.content)
        
        #if there was an exception it means the confirmation message wasn't valid (y/n).
        except Exception:
            #so we need to keep prompting until we don't get an exception
            while True:
                await ctx.send('invalid decision, enter y to proceed with the trade and n to cancel it.')
                print('invalid decision received, getting new decision')
                decision_msg = await self.client.wait_for('message', check=check)

                #check this decision again and break if we don't get an exception. Until that happens we'll just keep looping.
                try:
                    decision = helpers.get_confirmation(decision_msg.content)
                    break
                except Exception:
                    continue

        #cancel if the user said no.
        if decision == False:
            await ctx.send('trade cancelled.')
            print('trade cancelled by user')
            return
        
        #if we made it here, they confirmed their cancellation! So let's find it in the requests list and remove it.
        for i in range(len(self.open_trade_requests)):
            if self.open_trade_requests[i] == selected_request:
                self.open_trade_requests.pop(i)
                print('request deleted!')

        await ctx.send('request deleted!')
        return

#this must be present at the end of every cog file to make it work. don't ask me why. it's just how it is. like how the sky is blue (when there isn't a storm, and it's daytime) and how the sky is not blue otherwise.
async def setup(client):
    await client.add_cog(Trading(client))