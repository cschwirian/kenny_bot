# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import platform
import random
import requests
import json
import league_api
import os

from discord.ext.commands import Bot
from discord import Server
from discord.ext import commands

DISCORD_API_KEY = ""
with open( "config/discord_api_key.txt", "r" ) as config:
    DISCORD_API_KEY = config.readline().replace( "\n", "" )


# Here you can modify the bot's prefix and description and whether it sends help in direct messages or not.
client = Bot( description="Kenny in bot form.", command_prefix = "~", pm_help = False )


# Events
@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=371776'.format(client.user.id))
    print('--------')
    print('You are running Kenny Bot v1.0')
    print('Created by cschwirian')

@client.event
async def on_message( message ):
    await client.process_commands( message )



# System Commands
@client.command( pass_context = True)
@asyncio.coroutine
def __stop__( context ):
    if( context.message.author.id == "131579027659030528" ):
        yield from client.close()
    else:
        yield from client.say( "Uh uh uh. You're not allowed to do that." )

@client.command( pass_context = True)
@asyncio.coroutine
def __restart__( context ):
    if( context.message.author.id == "131579027659030528" ):
        yield from client.run( DISCORD_API_KEY )
    else:
        yield from client.say( "Uh uh uh. You're not allowed to do that." )

@client.command( pass_context = True )
@asyncio.coroutine
def __get_emojis__( context ):
    print( "Emojis for server {} ({}):".format( context.message.server.id, context.message.server.name ) )

    emojis = context.message.server.emojis
    for index in range( len( context.message.server.emojis ) ):
        print( "    " + emojis[index].name + " - " + emojis[index].id )
    yield



# Commands
@client.command( description = "Says \"hey\". Pretty straightforward." )
@asyncio.coroutine
def hey( *args ):
    yield from client.say( "hey" )

@client.command( description = "Provides a link to the repository for kenny_bot." )
@asyncio.coroutine
def repo( *args ):
    yield from client.say( "https://github.com/cschwirian/kenny_bot" )

@client.command( pass_context = True, description = "For when a message needs a little more of that je ne sais quoi." )
@asyncio.coroutine
def improve( context, *, message ):
    if( str( message ).lower() == "kenny"):
        yield from client.say( "Cannot be improved." )
    else:
        message_str = str( message ).replace( "b", ":b:" ).replace( "B", ":b:" )
        yield from client.say( message_str )

# TODO: Random image
@client.command( pass_context = True )
@asyncio.coroutine
def pic( context ):
    pic = random.choice( os.listdir( "./images/pics" ) )
    yield from client.send_file( context.message.channel, "./images/pics/" + pic )

# TODO: Random image of Kenny - credit Miles
@client.command( pass_context = True )
@asyncio.coroutine
def kennypic( context ):
    pic = random.choice( os.listdir( "./images/kenny" ) )
    yield from client.send_file( context.message.channel, "./images/kenny/" + pic )

# TODO: Kenny quote of the day
@client.command()
@asyncio.coroutine
def quote():
    yield from client.say( "I've been getting Yasuo in ARAM a lot recently." )

@client.command( pass_context = True )
@asyncio.coroutine
def chill_gif( context ):
    gif = random.choice( os.listdir( "./gifs/chill" ) )
    yield from client.send_file( context.message.channel, "./gifs/chill/" + gif )

# TODO: Music

# TODO: Memes
# TODO: personalized memes

# TODO: Dice roll and other math
@client.command( pass_context = True, description = "Rolls some dice. Use the format \"~dice xdy\" where x is the number of y sided dice. d is d." )
@asyncio.coroutine
def roll( context, *, message ):
    try:
        message_str = str( message ).lower()
        split_message = message_str.split( "d" )
        num_dice = int( split_message[0] )
        num_sides = int( split_message[1] )

        if( num_dice > 64 ):
            yield from client.say( "I can't hold all those dice there, friend." )
        elif ( num_sides > 1000000 ):
            yield from client.say( "That's an unnecessarily large number, friend." )
        else:
            total_roll = 0
            for die in range( num_dice ):
                total_roll += random.randint( 1, num_sides )

            yield from client.say( "You rolled a %d." % total_roll )

    except:
        yield from client.say( "You messed up the roll somehow. None of my business." )

@client.command()
@asyncio.coroutine
def what():
    yield from client.say( "Hey, buddy. I'm Kenny. Type \"~hey\" or type \"~help\" to see what I can do." )

@client.command( pass_context = True, description = "Retrieves a player's winrate with a specific champion. Use the form \"~wr summoner/champion/queue/season\". queue and season optional." )
@asyncio.coroutine
def wr( context, *, message ):
    try:
        message_split = message.split( "/" )
        summoner_name = message_split[0]
        champion = message_split[1]

        if( len( message_split ) == 2 ):
            yield from client.say( league_api.get_winrate( summoner_name, champion, "", "" ) )
        elif( len( message_split ) == 3 ):
            queue = message_split[2]
            yield from client.say( league_api.get_winrate( summoner_name, champion, queue, "") )
        else:
            queue = message_split[2]
            season = message_split[3]
            yield from client.say( league_api.get_winrate( summoner_name, champion, queue, season) )
    except:
        yield from client.say( "Yeah, you messed that one up, buddy." )

@client.command( pass_context = True, description = "Retrieves a player's winrate with a specific champion for the current ranked season. Use the format \"wr summoner/champion\". Only works for NA." )
@asyncio.coroutine
def rwr( context, *, message ):
    try:
        message_split = message.split( "/" )
        summoner_name = message_split[0]
        champion = message_split[1]

        yield from client.say( league_api.get_current_ranked_winrate( summoner_name, champion ) )
    except:
        yield from client.say( "Yeah, you messed that one up, buddy." )

# Main
if( __name__ == "__main__" ):
    client.run( DISCORD_API_KEY )
