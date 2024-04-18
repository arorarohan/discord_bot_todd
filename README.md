# Todd the dog: a discord bot
Just a bot I made to mess around with, with my friends. Not really intended to be plug-and-play for others

## requirements
- python3
- discord.py library
- ffmpeg installed and added to PATH
- a private_config.py file with a discord API key (DISCORD_TOKEN, str) and welcome channel ID (str)


## usage - commands (keyword is 'todd' followed by a space)
### text commands
- hi - says hi
- mostenire_list - gives a list of words from mostenire_list.csv
- mostenire_add - adds mostenires to the list.
- file_of_shame - prints the file of shame, a list of messages sent by TARGETED_USER

### audio commands
- join - joins the voice channel of the user who sent the message
- play - play an item from /audio according to its keyword in AUDIO_DIRECTORY
- pause - pause playback
- stop - stop playback
- resume - resume playback
- leave - leave the voice channel
- playlist - display the playlist of items to play

## usage - events
- on_member_join - will greet new members in WELCOME_CHANNEL
- on_message - will save a message to file_of_shame.txt if sent by TARGETED_USER and will let them know they suck.
- on_member_remove - says bye to members who leave the server in WELCOME_CHANNEL

## learnings
- discord API
- decorators
- async programming
- OOP