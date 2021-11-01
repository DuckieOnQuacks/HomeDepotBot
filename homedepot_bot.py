# https://discord.com/api/oauth2/authorize?client_id=860542014214242354&permissions=238221312&scope=bot 
#add link ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

###Libraries###
import re
import os
import time
import pickle
import random
import discord
import asyncio

from discord.ext import tasks
from datetime import datetime
from dotenv import load_dotenv
from asyncio.tasks import sleep
from discord.ext import commands
from discord.errors import NotFound

###My Scripts###
import cputemp
import bookfinder
import fact_finder
import music_grabber
import image_request
import comment_search
import music_downloader
import youtube_song_link
import make_command

###Enviorment Paths###
import os
from pathlib import Path


ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

load_dotenv()

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("TOKEN")

intents = discord.Intents().default()
client = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    now = str(datetime.now().time()).split(".", 1)[0]
    print(now,"Bot Initialized")
    fact_message.start()
    game_status.start()
    purge_files.start()


#COMMAND FUNCTIONS

@client.event
async def on_message(message):
    now = str(datetime.now().time()).split(".", 1)[0]
    if message.author == client.user:
        return
    print(now,"Incoming Message From " + str(message.guild))

    
    if message.content.startswith('useless bot'):
        name = str(message.author).split('#', 1)[0]
        await message.channel.send("HomeDepot bot recommends you sleep with your eyes open.")
        waittime = random.randint(10,30)
        print(now,"Waiting " + str(waittime) + " seconds and sending dm to " + name)
        await asyncio.sleep(waittime)
        await message.author.create_dm()
        await message.author.dm_channel.send(f'IM GOING TO FUCKING MURDER YOU {name}')
        print(now,"Sent dm")

    if message.content.startswith('what kind of day is it'):
        num = random.randint(0,1)
        if(num == 1):
            await message.channel.send("Today will be a bones day")
        else:
            await message.channel.send("Today is a no bones day")

    if message.content.startswith('hello'):
        name = str(message.author).split('#', 1)[0]
        await message.channel.send('Sup  ' + name)
            
    await client.process_commands(message)
    
##################################### TUNES ###########################################################
#This function, with the use of a last.fm account, will give you youtube links to songs that fit your
#music genres based off of spotify.
#######################################################################################################
@client.command()
async def tunes(cxt, search=None):
        server = cxt.guild
        name = str(cxt.author).split('#', 1)[0]
        print(name)
        if search == None:
            music_grabber.usersearch(name)
            
            if music_grabber.found:
                username = music_grabber.username
                print(username)
                await cxt.invoke(client.get_command('play'), search = music_grabber.get_song_list(username))
                await cxt.channel.send("https://"+music_grabber.get_song_list(username))
            else:
                await cxt.channel.send("Repeat the command and add your last.fm username")
        else:
           music_grabber.useradd(name, search)
           await cxt.channel.send("Adding " + name + " " + search)
           



##################################### Make ###########################################################
#Grabs recepies off all receipies website
#Prints ingredients then directions if any
#######################################################################################################
@client.command()
async def make(cxt, *, search = None):
    if search == None:
        await cxt.channel.send("You must type something after $make")
    else:
        await make_command.getmakelink(search)
        link = make_command.link
        await make_command.getimage(link)
        image = make_command.image
        returnedobject = "".join(link.split("/")[5]).replace("-"," ")
        await make_command.getingredients(link)
        try:
            await make_command.getdirections(link)
            directions = make_command.directions
        except:
            directions= "___***SOME IDIOT DIDNT PUT THE DIRECTIONS, THEY ARE PROBABLY IN THE DISCRIPTION***___"
        ingredients = make_command.ingredients
        await cxt.channel.send("___***"+returnedobject+"***___")
        await cxt.channel.send(image)
        await cxt.channel.send(ingredients)
        await cxt.channel.send(directions)
                     

    
##################################### STOP ###########################################################
#This function stops whatever ear rape is being played
######################################################################################################
@client.command()
async def stop(cxt):
        server = cxt.guild
        print("halting voice")
        try:
            try:
                await server.voice_client.disconnect()
            except AttributeError:
                print("Not in a voice channel")
        except:
            print("Error leaving voice channel")

        
##################################### TEMPRATURE #####################################################
#Simple temprature command that tells you the conditions of home depots house. (Raspberry pi 3B+)
######################################################################################################                
@client.command()
async def TEMP(cxt):
        await cputemp.gettemp()
        await cxt.channel.send("Temp is "+str(cputemp.cpu_temp))

        
##################################### PLAY ###########################################################
#Function that plays whatever your heart desires at the push of a button. (as long as its on youtube)
######################################################################################################
@client.command()
async def play(cxt, * , search):
        server = cxt.guild
        name = cxt.author
        if not cxt.author.voice:
            await cxt.channel.send(name + " is not connected to a voice channel")
            return
        else:
            channel = cxt.author.voice.channel
        try:
            await channel.connect()

            if "https" not in search:
                youtube_link = youtube_song_link.get_song_url(search)
                if("channel" in youtube_link):
                    await cxt.channel.send("Fuck you, you got a channel link")
                else:   
                    await music_downloader.download(youtube_link)
                    await cxt.channel.send("__***Playing: "+music_downloader.audioname+"***__")
                    
                    print(music_downloader.audiofile)
                    print(os.getcwd()+"/tmp/" + music_downloader.audiofile)
            else:
                await music_downloader.download(search)
                await cxt.channel.send("__***Playing: "+music_downloader.audioname+"***__")
                print(music_downloader.audiofile)
                print(os.getcwd()+"/tmp/" + music_downloader.audiofile)

                
            server.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=os.getcwd()+"/tmp/" + music_downloader.audiofile))
            await asyncio.sleep(music_downloader.audiolength + 5)
            if server.voice_client.is_connected():
                await server.voice_client.disconnect()
            else:
                return
            await asyncio.sleep(round(music_downloader.audiolength+(music_downloader.audiolength*.3)))
            os.remove(os.getcwd()+"/tmp/" + music_downloader.audiofile)
            print("REMOVED FILE " + os.getcwd()+"/tmp/" + music_downloader.audiofile)
        except:
            print("CHANNEL ERROR")
            await cxt.message.channel.send("Already in a voice channel")
            return
            

#####################################       QUEUE      #######################################
#queue
##############################################################################################

@client.command()
async def queue(cxt, * , search):
    server = cxt.guild
    index = 1
    while True:
        if server.voice_client.is_playing():
            return
        else:
            await cxt.invoke(client.get_command('play'), search=search)
            break


            
##################################### HOME DEPOT BUILD #######################################
#Function that ear rapes you with the wonderful song of the poeple.
############################################################################################# 
@client.command()
async def build(cxt):
        name = str(cxt.author).split('#', 1)[0]
        await cxt.channel.send(name + " would like to build some shit")
        server = cxt.guild
        if not cxt.author.voice:
            await cxt.channel.send(name + " is not connected to a voice channel")
            return
        else:
            channel = cxt.author.voice.channel
        try:
            await channel.connect()
        except:
            print("channel error")
            await cxt.channel.send("Already in a voice channel")
        server.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="depot.mp3"))
        await asyncio.sleep(20)
        if server.voice_client.is_connected():
            await server.voice_client.disconnect()
        else:
            return


##################################### HOME DEPOT CHILL #######################################
#Function that chills you out colder than home depots layaway freezers
#############################################################################################   
@client.command()      
async def chill(cxt):
        name = str(cxt.author).split('#', 1)[0]
        await cxt.channel.send(name + " sit back, relax and enjoy")
        server = cxt.guild
        if not cxt.author.voice:
            await cxt.channel.send(name + " is not connected to a voice channel")
            return
        else:
            channel = cxt.author.voice.channel
        try:
            await channel.connect()
        except:
            print("channel error")
            await cxt.channel.send("Already in a voice channel")
        server.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="homedepotlofi.mp3"))
        await asyncio.sleep(82)
        if server.voice_client.is_connected():
            await server.voice_client.disconnect()
        else:
            return


##################################### YODAS TEACHINGS #######################################
#Function that voices the teachings of the green lightsaber weilding master yoda.
#############################################################################################
@client.command()
async def yoda(cxt):
        name = str(cxt.author).split('#', 1)[0]
        server = cxt.guild
        listmp3 = ["yodabust.mp3", "stinka.mp3", "yodacrush.mp3"]
        if not cxt.author.voice:
            await cxt.channel.send(name + " is not connected to a voice channel")
            return
        else:
            channel = cxt.author.voice.channel
        try:
            await channel.connect()
        except:
            print("channel error")
            await cxt.channel.send("Already in a voice channel")
        server.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source= listmp3[random.randint(0,len(listmp3)-1)]))
        await asyncio.sleep(18)
        if server.voice_client.is_connected():
            await server.voice_client.disconnect()
        else:
            return


##################################### LEAGUE LANE ###########################################
#Function that when promted, gives you a random league of legends lane to play in.
#############################################################################################        
@client.command()
async def league(cxt):
        name = str(cxt.author).split('#', 1)[0]
        lanelist = ["TOP","MIDDLE","BOTTOM", "SUPPORT","JUNGLE"]
        yourlane = lanelist[random.randint(0,4)]
        await cxt.channel.send(name + " should go " + yourlane.lower())
        

##################################### BOOK SEARCH ###########################################
#Function that when promted, gives you a random book from and array of books.
#############################################################################################
@client.command()
async def search(cxt, books = None):
    if books == "books":
        bookfinder.booksearch()
        commentlist = ["A great read" , "My personal favorite", "A modern day shakespear" , "This story is life-changing", "A god given masterpiece","kill me"]
        bookimage = bookfinder.booklink
        await cxt.channel.send(bookimage)
        await cxt.channel.send(commentlist[random.randint(0,len(commentlist) - 1)])
    else:
        print("Invalid Book Entry")
        

##################################### BLESS ME ###########################################
#Function that when promted, gives you a random comment from and array of pornhub links.
##########################################################################################   
@client.command()
async def bless(ctx, me = None):
    if me == "me":
        await comment_search.givecomment()
        await ctx.channel.send(comment_search.retcomment)
        print("printing a comment")
    else:
        print("Invalid bless command")

    
##################################### GIMME ################################################
#Function that depending on what the user enters after the .gimme command will find a random
#image of that item and post it in the chat.
############################################################################################  
@client.command()
async def gimme(ctx, search = None):
        image_request.imagesearch(search)
        image = image_request.retlink
        await ctx.channel.send(image)
        await ctx.channel.send("__***" + image_request.actualsearch.upper() + "***__")
        
        
##################################### CLEAR #################################
#Function to clear out a certain amount of messages that is given by the user
#Default value for number of messages deleted is 5 - 1 because of the clear
#command itself if not otherwise specified
############################################################################# 
@client.command()
async def clear(ctx, amount = 5):
        try:
            await ctx.channel.purge(limit = amount)
            await ctx.channel.send(amount + " messages deleted")
        except:
           await ctx.channel.send("Invalid Amount") 
    

#DM ON MEMBER JOIN===================================================================================================================
@client.event
async def on_member_join(member):
    await member.create_dm()
    image_request.imagesearch("cat")
    await member.dm_channel.send(f'Hi {member.name}, HomeDepot bot welcomes you, It is too late to turn back')
    await member.dm_channel.send(  f'' + image_request.retlink)

#LOOPS ==============================================================================================================================
@tasks.loop(seconds=60)
async def fact_message():
    now = str(datetime.now().time()).split(".", 1)[0]
    waittime = random.randint(86400,172800)
    print(now,"fact_message waiting " + str(round((waittime)/60)) + " minutes to send")
    await asyncio.sleep(waittime)
    fact_finder.givefact()
    fact = fact_finder.fact
    now = str(datetime.now().time()).split(".", 1)[0]
    print(now,"sending fact")
    await client.get_channel(729895104101351457).send(fact)

@tasks.loop(seconds=600)
async def purge_files():
    now = str(datetime.now().time()).split(".", 1)[0] 
    print(now,"Purging....")
    now = time.time()

    for filename in os.listdir(os.getcwd()+"/tmp"):

        if os.path.getmtime(os.path.join(os.getcwd()+"/tmp", filename)) < now - 3600:
            if os.path.isfile(os.path.join(os.getcwd()+"/tmp", filename)):
                print("Removed: "+filename)
                os.remove(os.path.join(os.getcwd()+"/tmp", filename))
        elif os.path.getmtime(os.path.join(os.getcwd()+"/tmp", filename)) >= now - 3600:
            print("Ignoring: "+ filename)

# STATUS LIST=========================================================================================================================
status_list = ["I love Man-Milk.","God is cruel.","Kris is gay.","mmm Man-Milk delicious","Please Help Me..."]
@tasks.loop(seconds=60)
async def game_status():
        index = 0
        while index < len(status_list):
            await client.change_presence(status=discord.Status.online, activity=discord.Game(status_list[index]))
            await asyncio.sleep(60)
            index = index + 1

client.run(TOKEN)


