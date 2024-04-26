#games you can play with todd! more than just standard-response text commands.

import discord
from discord.ext import commands
import random
from scripts import helpers
from scripts.dictionaries import Dictionaries

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        #use instance variables to store things that we want to track across multiple command calls.
        self.farts = 0
        self.ongoing_guessing_games = {}

    ########################################################### FART GAME################################################################################################
    #####################################################################################################################################################################

    @commands.command(brief='make todd fart! see how long he can hold his poop')
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

                #first dole out the user's reward
                reward = int(poop_chance * 10)
                helpers.update_balance(ctx.author.name,reward)
                new_bal = helpers.check_balance(ctx.author.name)

                #then give them their output
                with open('assets/poop.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)
                await ctx.send(f"I just pooped (had a {int(poop_chance * 100)}% chance of doing so). todd say oops.\nYou earned {reward} toddallions! Balance: {new_bal}")
                print(f"pooped at {poop_chance}")
                
                #finally, reset the game by setting farts to 0
                self.farts = 0
            
            #if they aren't pooping, we process the fart
            else:
                #increment the fart count
                self.farts += 1

                #give the user the output
                await ctx.send(f"farted! I have farted {self.farts} times so far. I had a {int(poop_chance * 100)}% chance of pooping just now, but i didn't. todd sighs in relief.")
                print(f"farted {self.farts} times at {poop_chance}")

    
    ############################################ FETCH GAME ###################################################################################################
    ###########################################################################################################################################################

    @commands.command(brief='todd fetches stuff! good boy')
    async def fetch(self, ctx):
        
        #instantiate a dictionaries object, and load the fetchables
        dictionaries = Dictionaries()
        dictionaries.load_fetchables()
        #get our fetchables dictionary from it
        fetchables = dictionaries.fetchables

        #now let's determine which item has been fetched!
        #random.choices() does not take DictKeys or DictValues as inputs so we have to convert them to lists first.
        fetchable_items = [key for key in fetchables.keys()]
        fetchable_weights = [value['probability'] for value in fetchables.values()]
        #the output of this function is a list with (in this case) 1 element, so we select the element to get a string
        fetched_item = random.choices(fetchable_items,fetchable_weights)[0]
        
        #add the user to the hall of fame if they got gold, or add to the drew sharp count if it was a spider
        if fetched_item == 'gold':
            helpers.add_to_hof(ctx.author.name)
            print('added the user to hall of fame!')
        elif fetched_item == 'spider in a jar':
            helpers.shoot_drew_sharp()
            print('shot drew sharp.')
        

        #update their balance according to what they got, if their is something to add
        if fetchables[fetched_item]['value'] is not None:
            helpers.update_balance(ctx.author.name,fetchables[fetched_item]['value'])
            new_bal = helpers.check_balance(ctx.author.name)

        #send an image according to the fetched item, if there is one
        if fetchables[fetched_item]['image'] is not None:
            with open(fetchables[fetched_item]['image'],'rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
        
        #send the message according to what was fetched.
        await ctx.send(fetchables[fetched_item]['message'])
        print(f"fetched {fetched_item} with a {fetchables[fetched_item]['probability']} chance for {fetchables[fetched_item]['value']} Toddallions")

        #send toddallions message only if toddallions were added
        if fetchables[fetched_item]['value'] is not None:
            await ctx.send("you earned {0} toddallions! Balance: {1}".format(fetchables[fetched_item]['value'], new_bal))


    ##################################### GUESSING GAME ######################################################################################
    #########################################################################################################################################

    # todd will have a number (1-100) in his head. You need to guess what it is!
    # todd will tell you if you're higher or lower than the answer. Your score is the number of guesses you took to get todd's number!
    @commands.command(brief='guess todd\'s number!')
    async def guessing_game(self,ctx):
        #check if this user is in the dictionary, and if so, check if they are playing the game. This block is to prevent a single user playing multiple instances of the game simultaneously.
        if ctx.author.name in self.ongoing_guessing_games.keys():
            
            #if they are already playing the game, ask them to continue and don't proceed to execute the rest of the method. If they aren't, we just continue
            if self.ongoing_guessing_games[ctx.author.name] == True:
                await ctx.send('you are already playing the game! Make a guess to continue playing.')
                print('could not start the game as the user is already playing')
                #return from the method to prevent the rest of the code from executing.
                return
    
        #if we made it past that block, it means either the user isn't in the dict or they have played before but aren't currently playing. Either way, we are good to go.
        #let's start by recording that this user's game has started, and initializing our overriden variable
        overridden = False
        self.ongoing_guessing_games[ctx.author.name] = True

        #now let's prompt the user to start the game!
        await ctx.send("We're going to play a guessing game! I have an integer in my head between 1 and 100 inclusive. Start by taking a guess, I'll let you know if you're higher or lower! Note: I'll ignore you if you don't give me an integer. Type <cancel> to end the game at any time.")
        print('initiated guessing game')
        # let it be known that this is the moment I realized that higher-lower is a shit game because the best answer is just binary search.
        #let's first hold an answer in our head
        answer = random.randint(1,100)
        
        #define a checking function for our guesses: just check that the author is the person that initiated the interaction, and they have given us an integer.
        def check(m):
            #check if the user is trying to override, and let the message pass through if they are
            if m.content == 'cancel' and ctx.author.name == m.author.name:
                return True
            
            #if not, we proceed to check the validity of the message
            else:
                #try converting the message to an integer. If it doesn't work, it means the message wasn't an integer
                try:
                    content = int(m.content)
                except ValueError:
                    content = m.content
                return m.author.name == ctx.author.name and isinstance(content, int)
        
        #get our first guess
        guess_msg = await self.client.wait_for('message', check=check)
        
        #check if the user is trying to cancel
        if guess_msg.content == 'cancel':
            overridden = True
        #if they aren't, we kickstart the game
        else:
            guess = int(guess_msg.content)
            score = 1
        
        #for some dumb reason if we don't check this BEFORE the loop, then if the user cancelled the game as their initial 'guess', we just get stuck here, neither entering nor skipping the while loop.
        if overridden == False:
            while (guess != answer) and (overridden == False):
                #give feedback on the answer
                if guess > answer:
                    await ctx.send("your guess was higher than the answer! go lower. Or use <cancel> to give up.")
                    print(f'wrong guess, {guess} > {answer}')
                else:
                    await ctx.send('your guess was lower than the answer! go higher. Or use <cancel> to give up.')
                    print(f'wrong guess, {guess} < {answer}')
                
                # get our next guess and increment the score if the user isn't trying to override.
                guess_msg = await self.client.wait_for('message', check=check)
                if guess_msg.content == 'cancel':
                    overridden = True
                else:
                    guess = int(guess_msg.content)
                    score += 1
        
        #exiting the while loop means either we got the answer, or the user tried to override! 
        #if the user performed an override, we end the game here.
        if overridden:
            await ctx.send('game cancelled!')
            print('guessing game cancelled by user!')
            self.ongoing_guessing_games[ctx.author.name] = False
        
        #if we're here and there wasn't an override, it means the user completed the game!
        else:
            
            #choose a message to send and reward to give according to the score
            #<=2 = star
            if score <= 2:
                reward = 15
                feedback_message = random.choice(["youre a genius fr br0 ","NO WAY!!SO SMARTY UWUWUWUs "])
                with open('assets/guessing_game/star.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)
            #<=5 = smiley
            elif score <= 5:
                reward = 7
                feedback_message = random.choice(["owowo not bad lad! ","okAYY OKAY we going for sth here "])
                with open('assets/guessing_game/smiley.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)
            #<=8 = neutral face
            elif score <= 8:
                reward = 3
                feedback_message = random.choice(["bro u actl kinda slow haha ","meh. u could do better fr "])
                with open('assets/guessing_game/neutral.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)
            #else = frowny
            else:
                reward = 1
                feedback_message = random.choice(["are u even trying HAHHAHA ","eh. lame :3 "])
                with open('assets/guessing_game/frowny.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)

            #now give the appropriate reward
            helpers.update_balance(ctx.author.name,reward)
            new_bal = helpers.check_balance(ctx.author.name)

            #then send the result message
            await ctx.send(f'you got it in {score} guesses! {feedback_message}. \n\nYou earned {reward} toddallions. New balance: {new_bal}')
            print(f'guessing game ended as {guess} = {answer}, score = {score}')
            self.ongoing_guessing_games[ctx.author.name] = False


    ################################################################ STEAL ###########################################################################
    ###################################################### IS THIS EVEN A GAME #############################################################################

    #you must pay 20 toddallions to participate in theft. todd will steal a number of toddallions from a targeted user between 0 to 40 or the amount they have, whichever is lower.
    @commands.command(brief='steal from another user! Use <todd steal @user>')
    async def steal(self, ctx, arg: discord.User):
        #by default this will ignore any argument that isn't of the valid type

        #now let's get our user data.
        thief_username = ctx.author.name
        thief_bal = helpers.check_balance(thief_username)
        victim_username = arg.name
        victim_bal = helpers.check_balance(victim_username)

        #let's figure out the maximum number of toddallions that can be stolen
        if victim_bal < 40:
            theft_limit = victim_bal
        else:
            theft_limit = 40
        
        #the thief can't steal if they can't put up the 20 toddallions.
        if thief_bal < 20:
            await ctx.send('you need to have at least 20 toddallions to fund this theft! Come again when you aren\'t as poor.')
            print('theft failed: not enough toddallions')
            return

        #can't steal if the victim has no toddallions.
        if victim_bal == 0:
            await ctx.send('you can\'t steal from that user, because their balance is zero! try again, but choose someone worth stealing from.')
            print('theft failed: victim has 0 toddallions')
            return
        
        #can't steal from yourself
        if victim_username == thief_username:
            await ctx.send('you can\'t steal from yourself! Please consider a more productive choice and try again.')
            print('theft failed: cannot steal from self.')
            return
        
        #can't steal from someone who is not in this server (it wouldn't be fair)
        #get a list of the mutual servers of todd and the victim. We will compare it to the name of this server
        mutuals = arg.mutual_guilds
        this_server = ctx.message.guild #the server the steal command was called in
        
        #we will search through every server in the mutuals list and compare its name to the name of the server the command was triggered from.
        in_server = False
        #don't bother searching if there are no mutual servers (this would happen if todo has been removed from the server the target user used to be in)
        if mutuals != []:
            #conduct the search and set in_server to True if we found this server in the list
            for server in mutuals:
                if server.name == this_server.name:
                    in_server = True
                    break

        #deal with the issue if the user really isn't in this server, and return from the method to stop the steal from continuing.
        if not in_server:
            await ctx.send('you can\'t steal from that user as they aren\'t in this server! either invite them (todd wants everyone to be together) or steal from someone else!')
            print('theft failed: victim not in server')
            return

        #if we can steal, we need to let the user know what they're in for.
        await ctx.send(f'Funding this theft requires you to spend 20 toddallions. You will steal an amount of toddallions between 0 and {theft_limit} from {victim_username}.\n{victim_username}\'s balance: {victim_bal}\nYour balance: {thief_bal}.\nContinue? (y/n)')
        
        #checking function to vet confirmation messages, so that only the thief can confirm.
        def check(m):
            return ctx.author.name == m.author.name

        #get the decision from the user
        decision_msg = await self.client.wait_for('message', check=check)
        
        #check the decision
        try:
            decision = helpers.get_confirmation(decision_msg.content)
        
        #if there was an exception it means the confirmation message wasn't valid (y/n).
        except Exception:
            #so we need to keep prompting until we don't get an exception
            while True:
                await ctx.send('invalid decision, enter y to proceed with the theft and n to cancel it.')
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
            await ctx.send('theft cancelled.')
            print('theft cancelled by user')
            return
        
        #if we got to this point, they said yes. So let's process the theft.
        
        #find out how much is stolen and get the profit (negative=loss)
        theft_amt = random.randint(0,theft_limit)
        profit = theft_amt - 20

        #make the account adjustments - the thief gains/loses the difference between the theft cost and the stolen amount, while the victim loses however much was stolen
        helpers.update_balance(thief_username, profit)
        new_thief_bal = helpers.check_balance(thief_username)

        helpers.update_balance(victim_username,-theft_amt) #a very important negative sign!
        new_victim_bal = helpers.check_balance(victim_username)

        #let's display the result!
        await ctx.send(f'You spent 20 toddallions to steal {theft_amt} from {victim_username}! Your profit (or loss) was {profit}.\nYour new balance: {new_thief_bal}.\n{victim_username}\'s new balance: {new_victim_bal}.')
        print(f'{thief_username} stole {theft_amt} from {victim_username}: profit = {profit}, thief balance changed from {thief_bal} to {new_thief_bal}, victim balance changed from {victim_bal} to {new_victim_bal}.')



#this must be present at the end of every cog file to make it work. don't ask me why. it's just how it is. like how the sky is blue (when there isn't a storm, and it's daytime) and how the sky is not blue otherwise.
async def setup(client):
    await client.add_cog(Games(client))