#games you can play with todd! more than just standard-response text commands.

import discord
from discord.ext import commands
import random
import main
import csv


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        #first we need our variable outside of the function.
        self.farts = 0

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
        #we want todd to be able to fetch from a variety of objects, with varying chances for each.
        fetchables = {
            'stick':0.2,
            'ball':0.17,
            'rat':0.15,
            'spider in a jar':0.07,
            'nothing':0.2,
            'face of god':0.01,
            'gold':0.02,
            'briefcase':0.08,
            'skull':0.1,
            }
        
        #now let's determine which one has been fetched!
        #random.choices() does not take DictKeys or DictValues as inputs so we have to convert them to lists first.
        fetchable_items = [key for key in fetchables.keys()]
        fetchable_weights = [value for value in fetchables.values()]
        #the output of this function is a list with (in this case) 1 element, so we select the element to get a string
        fetched_item = random.choices(fetchable_items,fetchable_weights)[0]
        
        #different messages according to the items fetched, all follow a generic pattern except for gold
        if fetched_item == 'stick':
            with open('assets/fetch/stick.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('Woof! todd just found a stick! good boy!')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")
        
        elif fetched_item == 'ball':
            with open('assets/fetch/ball.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('Bark! todd just found a ball! In the distance, you see exasperated tennis players yelling slurs at todd. good dog!')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")
        
        elif fetched_item == 'rat':
            with open('assets/fetch/rat.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('oh no! todd just found a rat! looks like it\'s only just died. todd grins maniacally, a murderous look in his eyes, and wags his tail furiously. attaboy!')
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")

        elif fetched_item == 'spider in a jar':
            with open('assets/fetch/spider_in_a_jar.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('todd wandered off into the New Mexico desert and returned with a spider in a jar. he seems emotionless and stoic, as if his mind is still out there among the dunes. i wonder what he saw...')
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
            print(f"fetched {fetched_item} with a {fetchables[fetched_item]} chance")
        
        elif fetched_item == 'skull':
            with open('assets/fetch/skull.png','rb') as image:
                to_send = discord.File(image)
                await ctx.send(file=to_send)
            await ctx.send('Todd comes trotting up to you with a human skull!')
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

    ##################################### GUESSING GAME ######################################################################################
    #########################################################################################################################################

    # todd will have a number (1-100) in his head. You need to guess what it is!
    # todd will tell you if you're higher or lower than the answer. Your score is the number of guesses you took to get todd's number!
    @commands.command()
    async def guessing_game(self,ctx):
        await ctx.send("We're going to play a guessing game! I have a number in my head between 1 and 100 inclusive. Start by taking a guess, I'll let you know if you're higher or lower!")
        print('initiated guessing game')
        # let it be known that this is the moment I realized that higher-lower is a shit game because the best answer is just binary search.
        #let's first hold an answer in our head
        answer = random.randint(1,100)
        
        #define a checking function for our guesses: just check that the author is the person that initiated the interaction, and they have given us an integer.
        def check(m):
            #try converting the message to an integer. If it doesn't work, it means the message wasn't an integer
            try:
                content = int(m.content)
            except ValueError:
                content = m.content
            return m.author.name == ctx.author.name and isinstance(content, int)
        
        #get our firt guess
        guess_msg = await self.client.wait_for('message', check=check)
        guess = int(guess_msg.content)
        score = 1
        
        while guess != answer:
            #wait for messages to be received, collect them only if they pass the checks
            if guess > answer:
                await ctx.send("your guess was higher than the answer! go lower")
                print(f'wrong guess, {guess} > {answer}')
            else:
                await ctx.send('your guess was lower than the answer! go higher')
                print(f'wrong guess, {guess} < {answer}')
            
            # get our next guess and increment the score
            guess_msg = await self.client.wait_for('message', check=check)
            guess = int(guess_msg.content)
            score += 1
        
        #exiting the while loop means we got the answer! later, let's use this space to choose a cute image to send depending on how well the user did.
            # if score < x then blablabla, elif blablabla
        
        #also, we still need a way for the user to abort the game, and for the game to timeout so it doesn't run in perpetuity if the user gives up.
        #we also need a way to prevent the same user from starting the game if they are already playing one instance of the game.

        #finally, end by informing the user of their score
        await ctx.send(f'you got it in {score} guesses!')
        print(f'guessing game ended as {guess} = {answer}, score = {score}')
        #we can extend this by sending fun congratulatory/demeaning depending on the score





        


#this must be present at the end of every cog file to make it work. don't ask me why. it's just how it is. like how the sky is blue (when there isn't a storm, and it's daytime) and how the sky is not blue otherwise.
async def setup(client):
    await client.add_cog(Games(client))