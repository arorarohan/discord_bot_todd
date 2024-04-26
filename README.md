# Todd the dog: a discord bot
Just a bot I made to mess around with, with my friends. You can clone the repo and set it up fairly easily, allowing you to host it from the command line on any computer that can install the required software, and then start adding it to servers. For example, I am hosting my version of it on a raspberry pi running linux.

Feel free to suggest changes and improvements.

## general requirements
- python3
- ffmpeg installed and added to PATH
- a .env file set up in the root folder of the repo. Look at "dotenv_example.py" for instructions on how to do this.

## module requirements - can be automatically satisfied using requirements.txt
- discord.py library 
- discord.py[voice] module
- python-dotenv module

## usage - commands (keyword is 'todd' followed by a space)
### text commands
- hi - says hi
- mostenire_list - gives a list of words from mostenire_list.csv
- mostenire_add - adds mostenires to the list.
- file_of_shame - prints the file of shame, a list of messages sent by TARGETED_USER
- github - embeds the github repo for todd!
- hall_of_fame - displays the current standings in the hall of fame
- pet - pet todd! he will return a randomized choice out of a few preset messages.
- drew_sharp - gets the number of drew sharps that have fallen to todd (i.e. the number of spiders encountered in the fetch game)

### audio commands
- join - joins the voice channel of the user who sent the message
- play - play an item from /audio according to its keyword in AUDIO_DIRECTORY
- pause - pause playback
- stop - stop playback
- resume - resume playback
- leave - leave the voice channel
- playlist - display the playlist of items to play

### games
- fart - todd will fart, after 3 farts he will start having a growing chance to poop. If he poops, the chance will reset. Earn toddallions according to how many farts todd held it for.
- fetch - todd will fetch an object and bring it to you. If he finds gold, you get into the hall of fame! Earn toddallions according to the rarity of the item found.
- guessing_game - basically higher/lower. Keep guessing till you get the number todd is thinking of! Earn toddallions according to how many guesses it took.
- steal - steal from another user! you need to invest 20 toddallions in this action, and can steal anywhere from 0 to 40.

### shopping
- shop - displays items in the shop
- balance - displays your balance in toddallions
- buy - buy an item from the shop (if you can afford it)
- inventory - display your inventory of items purchased from the shop!

### trading
- trade - takes a user (either @user or username) as an argument. guides you through creating a trade request with that user.
- trade_requests - allows you to see your outstanding incoming and outgoing trade requests.
- trade_accept - displays your incoming trade requests, allowing you to accept them. Inventory changes will take place immediately upon acceptance.
- trade_decline - displays your incoming trade requests, allowing you to delete them.

## usage - events
- on_member_join - will greet new members in WELCOME_CHANNEL
- on_message - will save a message to file_of_shame.txt if sent by TARGETED_USER and will let them know they suck.
- on_member_remove - says bye to members who leave the server in WELCOME_CHANNEL

## learnings
- discord API
- decorators
- async programming
- OOP
- storing data

## credits
- some art by https://www.youtube.com/mostenire
- some art and features by https://github.com/huitingloke