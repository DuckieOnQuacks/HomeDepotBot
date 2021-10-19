# https://discord.com/api/oauth2/authorize?client_id=860542014214242354&permissions=238221312&scope=bot 
#add link ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
import asyncio
from asyncio.tasks import sleep
import random
import discord
from discord.errors import NotFound
from discord.ext import commands
from discord.ext import tasks
import pickle
from datetime import datetime
import re


#my scripts
import image_request
import fact_finder
import bookfinder
import comment_search
import cputemp
import music_grabber

#grab token from binary
infile = open("api_id",'rb')
TOKEN = pickle.load(infile)
infile.close()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!',intents=intents)

client = discord.Client()

@client.event
async def on_ready():
    now = str(datetime.now().time()).split(".", 1)[0]
    print(now,"Bot Initialized")
    fact_message.start()
    game_status.start()


#COMMAND FUNCTIONS





@client.event
async def on_message(message):
    now = str(datetime.now().time()).split(".", 1)[0]
    if message.author == client.user:
        return
    print(now,"Incoming Message From " + str(message.guild))



    if message.content.startswith('$hello'):
        name = str(message.author).split('#', 1)[0]
        await message.channel.send('Sup  ' + name)


    if message.content.startswith('!STOP!'):
        server = message.guild
        print("halting voice")
        try:
            await server.voice_client.disconnect()
        except:
            print("homedepotbot not connected")
            
    if message.content.startswith('!TEMP!'):
        cputemp.gettemp()
        await message.channel.send("Temp is "+str(cputemp.cpu_temp))



#VOICE COMMANDS ===========================================================================================
    if message.content.startswith('give me my tunes'):
        name = str(message.author).split('#', 1)[0]
        await message.channel.send(name + " wants to get some tunes")
        server = message.guild
        if(name == "Noah Leighton"):
            final = music_grabber.get_song_list("nleighton11")
            await message.channel.send("https://"+final)
        elif(name == "DuckieOnQuack"):
            final = music_grabber.get_song_list("duckieonquack")
            await message.channel.send("https://"+final)
        else:
            await message.channel.send("This user does not have an account go make one")
            

    if message.content.startswith('build'):
        name = str(message.author).split('#', 1)[0]
        await message.channel.send(name + " would like to build some shit")
        server = message.guild
        if not message.author.voice:
            await message.channel.send(name + " is not connected to a voice channel")
            return
        else:
            channel = message.author.voice.channel
        try:
            await channel.connect()
        except:
            print("channel error")
            await message.channel.send("Already in a voice channel")
        server.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="depot.mp3"))
        await asyncio.sleep(20)
        if server.voice_client.is_connected():
            await server.voice_client.disconnect()
        else:
            return

    if message.content.startswith('im feelin chill'):
        name = str(message.author).split('#', 1)[0]
        await message.channel.send(name + " sit back and relax")
        server = message.guild
        if not message.author.voice:
            await message.channel.send(name + " is not connected to a voice channel")
            return
        else:
            channel = message.author.voice.channel
        try:
            await channel.connect()
        except:
            print("channel error")
            await message.channel.send("Already in a voice channel")
        server.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="homedepotlofi.mp3"))
        await asyncio.sleep(83)
        if server.voice_client.is_connected():
            await server.voice_client.disconnect()
        else:
            return
        
    if message.content.startswith('im feelin extra chill'):
        name = str(message.author).split('#', 1)[0]
        await message.channel.send(name + " sit back, relax and enjoy")
        server = message.guild
        if not message.author.voice:
            await message.channel.send(name + " is not connected to a voice channel")
            return
        else:
            channel = message.author.voice.channel
        try:
            await channel.connect()
        except:
            print("channel error")
            await message.channel.send("Already in a voice channel")
        server.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="lofi.mp3"))
        await asyncio.sleep(960)
        if server.voice_client.is_connected():
            await server.voice_client.disconnect()
        else:
            return

    if message.content.startswith('yoda'):
        name = str(message.author).split('#', 1)[0]
        server = message.guild
        listmp3 = ["yodabust.mp3", "stinka.mp3"]
        if not message.author.voice:
            await message.channel.send(name + " is not connected to a voice channel")
            return
        else:
            channel = message.author.voice.channel
        try:
            await channel.connect()
        except:
            print("channel error")
            await message.channel.send("Already in a voice channel")
        server.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source= listmp3[random.randint(0,len(listmp3)-1)]))
        await asyncio.sleep(18)
        if server.voice_client.is_connected():
            await server.voice_client.disconnect()
        else:
            return
#VOICE COMMANDS ===========================================================================================





    
    if message.content.startswith('who is kris'):
        await message.channel.send("Kris is a dirty Man whore")
        await asyncio.sleep(5)
        await message.channel.send("You're welcome")

    if ('penis') in message.content or ('PENIS') in message.content:
        name = str(message.author).split('#', 1)[0]
        await message.channel.send(name + " is gay")

    if message.content.startswith('wake up mommy'):
        await message.channel.send("I PISSED THE BED")

    if message.content.startswith('dad walks in'):
        await message.channel.send(":eyes:")
        await message.channel.send("https://c.tenor.com/zUsPiUP3pQQAAAAd/shrek-dancing.gif")

    if message.content.startswith('useless bot'):
        name = str(message.author).split('#', 1)[0]
        await message.channel.send("HomeDepot bot recommends you sleep with your eyes open.")
        waittime = random.randint(10,30)
        print(now,"Waiting " + str(waittime) + " seconds and sending dm to " + name)
        await asyncio.sleep(waittime)
        await message.author.create_dm()
        await message.author.dm_channel.send(f'IM GOING TO FUCKING MURDER YOU {name}')
        print(now,"Sent dm")

    if message.content.startswith('where do i go') or message.content.startswith('what lane') or message.content.startswith('what lane?') or message.content.startswith('league'):
        name = str(message.author).split('#', 1)[0]
        lanelist = ["TOP","MIDDLE","BOTTOM", "SUPPORT","JUNGLE"]
        yourlane = lanelist[random.randint(0,4)]
        await message.channel.send(name + " should go " + yourlane.lower())

    if message.content.startswith('search books'):
        bookfinder.booksearch()
        commentlist = ["A great read" , "My personal favorite", "A modern day shakespear" , "This story is life-changing", "A god given masterpiece","kill me"]
        bookimage = bookfinder.booklink
        await message.channel.send(bookimage)
        await message.channel.send(commentlist[random.randint(0,5)])

    if message.content.startswith('bless me'):
        comment_search.givecomment()
        await message.channel.send(comment_search.retcomment)
        print(now,"printing a comment")

    if message.content.startswith('gimme '):
        search= message.content.replace("gimme ", "")
        image_request.imagesearch(search)
        image = image_request.retlink
        await message.channel.send(image)
        await message.channel.send("__***" + image_request.actualsearch.upper() + "***__")


#DM ON MEMBER JOIN
@client.event
async def on_member_join(member):
    await member.create_dm()
    image_request.imagesearch("cat")
    await member.dm_channel.send(f'Hi {member.name}, HomeDepot bot welcomes you, It is too late to turn back')
    await member.dm_channel.send(  f'' + image_request.retlink)

#LOOPS
@tasks.loop(seconds=60)
async def fact_message():
    now = str(datetime.now().time()).split(".", 1)[0]
    waittime = random.randint(3600,20000)
    print(now,"fact_message waiting " + str(round((waittime)/60)) + " minutes to send")
    await asyncio.sleep(waittime)
    fact_finder.givefact()
    fact = fact_finder.fact
    now = str(datetime.now().time()).split(".", 1)[0]
    print(now,"sending fact")
    await client.get_channel(729895104101351457).send(fact)



# STATUS LIST
status_list = ["I love Man-Milk.","God is cruel.","Kris is gay.","mmm Man-Milk delicious"]
@tasks.loop(seconds=60)
async def game_status():
        index = 0
        while index < len(status_list):
            await client.change_presence(status=discord.Status.online, activity=discord.Game(status_list[index]))
            await asyncio.sleep(60)
            index = index + 1

client.run(TOKEN)


