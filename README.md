# Todd the dog: a discord bot
Just a bot I made to mess around with, with my friends. Not really intended to be plug-and-play for others, but you're welcome to try.

## requirements
- python3
- discord.py library including discord.py[voice] module
- ffmpeg installed and added to PATH
- python-dotenv library
- NOTE - the above requirements can be satisfied using the requirements.txt file provided in the root folder.
- a .env file set up. Look at "dotenv_example.py" for instructions on how to do this.


## usage - commands (keyword is 'todd' followed by a space)
### text commands
- hi - says hi
- mostenire_list - gives a list of words from mostenire_list.csv
- mostenire_add - adds mostenires to the list.
- file_of_shame - prints the file of shame, a list of messages sent by TARGETED_USER
- github - embeds the github repo for todd!
- hall_of_fame - displays the current standings in the hall of fame

### audio commands
- join - joins the voice channel of the user who sent the message
- play - play an item from /audio according to its keyword in AUDIO_DIRECTORY
- pause - pause playback
- stop - stop playback
- resume - resume playback
- leave - leave the voice channel
- playlist - display the playlist of items to play

### games
 - fart - todd will fart, after 3 farts he will start having a growing chance to poop. If he poops, the chance will reset.
 - fetch - todd will fetch an object and bring it to you. If he finds gold, you get into the hall of fame!

## usage - events
- on_member_join - will greet new members in WELCOME_CHANNEL
- on_message - will save a message to file_of_shame.txt if sent by TARGETED_USER and will let them know they suck.
- on_member_remove - says bye to members who leave the server in WELCOME_CHANNEL

## learnings
- discord API
- decorators
- async programming
- OOP