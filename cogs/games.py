#games you can play with todd! more than just standard-response text commands.

import discord
from discord.ext import commands
import random
import main
import csv
import helpers

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        #use instance variables to store things that we want to track across multiple command calls.
        self.farts = 0
        self.ongoing_guessing_games = {}

    ########################################################### FART GAME################################################################################################
    #####################################################################################################################################################################

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

    
    ############################################ FETCH GAME ###################################################################################################
    ###########################################################################################################################################################

    @commands.command()
    async def fetch(self, ctx):
        #we want todd to be able to fetch from a variety of objects, with varying chances for each. format is item:[probability,value]
        fetchables = {
            'stick':[0.2, 1],
            'ball':[0.17, 1],
            'rat':[0.15, 2],
            'spider in a jar':[0.07, 5],
            'nothing':[0.2, 0],
            'face of god':[0.01, 0],
            'gold':[0.02, 20],
            'briefcase':[0.08, 4],
            'skull':[0.1,3]
            }
        
        #now let's determine which one has been fetched!
        #random.choices() does not take DictKeys or DictValues as inputs so we have to convert them to lists first.
        fetchable_items = [key for key in fetchables.keys()]
        fetchable_weights = [value[0] for value in fetchables.values()]
        #the output of this function is a list with (in this case) 1 element, so we select the element to get a string
        fetched_item = random.choices(fetchable_items,fetchable_weights)[0]

        #add the rewards to the user's balance and check what it has become
        helpers.update_balance(ctx.author.name,fetchables[fetched_item][1])
        new_bal = helpers.check_balance(ctx.author.name)
        
        #different messages and rewards according to the items fetched, all follow a generic pattern except for gold
        if fetched_item == 'stick':
            with open('assets/fetch/stick.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('Woof! todd just found a stick! good boy!')
            await ctx.send(f'you earned {fetchables[fetched_item][1]} toddallions! Balance: {new_bal}')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item][0]} chance for {fetchables[fetched_item][1]} Toddallions")
        
        elif fetched_item == 'ball':
            with open('assets/fetch/ball.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('Bark! todd just found a ball! In the distance, you see exasperated tennis players yelling slurs at todd. good dog!')
            await ctx.send(f'you earned {fetchables[fetched_item][1]} toddallions! Balance: {new_bal}')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")
        
        elif fetched_item == 'rat':
            with open('assets/fetch/rat.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('oh no! todd just found a rat! looks like it\'s only just died. todd grins maniacally, a murderous look in his eyes, and wags his tail furiously. attaboy!')
            await ctx.send(f'you earned {fetchables[fetched_item][1]} toddallions! Balance: {new_bal}')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")

        elif fetched_item == 'spider in a jar':
            with open('assets/fetch/spider_in_a_jar.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('todd wandered off into the New Mexico desert and returned with a spider in a jar. he seems emotionless and stoic, as if his mind is still out there among the dunes. i wonder what he saw...')
            await ctx.send(f'you earned {fetchables[fetched_item][1]} toddallions! Balance: {new_bal}')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")

        elif fetched_item == 'nothing':
            await ctx.send('todd searched far and wide, and came back empty-handed. you call him a bad dog and storm off, but todd whimpers and follows you closely. he may not be smart, but he sure is loyal.')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")
        
        elif fetched_item == 'face of god':
            with open('assets/fetch/face_of_god.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('Todd stumbles back to you. Initially, you think he just failed to find anything and came back quickly, but then you look closer into his eyes. They seem to be hollow, soulless, like he\'s seen something he cannot describe to you. \"I saw the face of God,\" Todd said, \"A distant vision from behind the clouds. The heavenly bells and choir sounded, rang in my ears, a cacaphony of holiness I was unfit of witnessing. His Eye watched me, judging me.\" Todd shivers. \"I dare not envision it even now, lest I fall back into despair. What felt like seconds for you was years for me. The bells still ring. I fear they will continue to ring till I am gone. And when the last of my ashes is incinerated, and the universe breathes its last, that unceasing melody will only get louder.\"')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")
        
        elif fetched_item == 'briefcase':
            with open('assets/fetch/briefcase.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('Hmm... todd just found a strange, black briefcase. Maybe best not to open it for now.')
            await ctx.send(f'you earned {fetchables[fetched_item][1]} toddallions! Balance: {new_bal}')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")
        
        elif fetched_item == 'skull':
            with open('assets/fetch/skull.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('Todd comes trotting up to you with a human skull!')
            await ctx.send(f'you earned {fetchables[fetched_item][1]} toddallions! Balance: {new_bal}')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")

        #if todd fetches gold, we want to induct the user to the hall of fame along with their score.
        elif fetched_item == 'gold':
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")

            #now for the hall of fame bit
            #grab the username
            username = ctx.message.author.name

            #first see if our user already exists in the hall of fame
            with open(main.FAME_PATH,'r') as file:
                items = list(csv.reader(file))
            
            idx_to_change = -1
            for row_idx in range(len(items)):
                if items[row_idx][0] == username:
                    idx_to_change = row_idx
                    break
            
            #if we found the username in our list, idx_to_change would be >= 0.
            #in the case that the user is a first-timer to our list, we want to add them as a new row:
            if idx_to_change < 0:
                with open(main.FAME_PATH,'a',newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([username, '1'])
                print("added the user to HOF as a new entry")
                
            
            #in the case that the user is already in the list, we want to replace the list with a new set of items that has the row with our user updated:
            else:
                #update our value
                new_number = int(items[idx_to_change][1]) + 1
                items[idx_to_change][1] = str(new_number)

                #write it to the file
                with open(main.FAME_PATH,'w',newline='') as file:
                    writer = csv.writer(file)
                    
                    for item in items:
                        writer.writerow(item)
                print("updated the user's score!")

            #and now for our output!
            with open('assets/fetch/gold.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('Bark! Yap! Run in circles! jubilation! todd just found a bar of gold! he drops it and it lands squarely on your big toe, and you convulse in pain on the ground, grinning with pride as todd licks your face enthusiastically. \nYour score has been inducted into the hall of fame! Use <todd hall_of_fame> to see highscores.')
            await ctx.send(f'you earned {fetchables[fetched_item][1]} toddallions! Balance: {new_bal}')

    ##################################### GUESSING GAME ######################################################################################
    #########################################################################################################################################

    # todd will have a number (1-100) in his head. You need to guess what it is!
    # todd will tell you if you're higher or lower than the answer. Your score is the number of guesses you took to get todd's number!
    @commands.command()
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
            if m.content == 'cancel':
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
            #choose an image to send according to the score
            #<=2 = star
            if score <= 2:
                with open('assets/guessing_game/star.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)
            #<=5 = smiley
            elif score <= 5:
                with open('assets/guessing_game/smiley.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)
            #<=8 = neutral face
            elif score <= 8:
                with open('assets/guessing_game/neutral.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)
            else:
                with open('assets/guessing_game/frowny.png','rb') as image:
                    to_send = discord.File(image)
                    await ctx.send(file=to_send)
            #else = frowny

            #then send the result message
            await ctx.send(f'you got it in {score} guesses!')
            print(f'guessing game ended as {guess} = {answer}, score = {score}')
            self.ongoing_guessing_games[ctx.author.name] = False


#this must be present at the end of every cog file to make it work. don't ask me why. it's just how it is. like how the sky is blue (when there isn't a storm, and it's daytime) and how the sky is not blue otherwise.
async def setup(client):
    await client.add_cog(Games(client))