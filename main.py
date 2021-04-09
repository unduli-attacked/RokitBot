import discord
import os
import fun
import pytz
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('r!'):
        # is command
        commandList = [
            ["nextLaunch", "Sends data on the next rocket to launch."],
            ["prevLaunch", "Sends data on the most recent rocket launch."],
            ["getLaunch [keyword]", "Searches for a launch and returns data if found."],
            ["nextEvent", "Sends data on the next space event."],
            ["prevEvent", "Sends data on the most recent space event."],
            ["getEvent [keyword]", "Searches for an event and returns data if found."]
        ]
        command = message.content[2:].lower() # lowercase command name
        print(command)
        if command == "help":
            toSend = ""
            for commandDescrip in commandList:
                toSend += "**{}:** {}\n\n".format(commandDescrip[0], commandDescrip[1])
            await message.channel.send(toSend)
        elif command == "nextlaunch":
            await message.channel.send(fun.getNextLaunch())
            # next launch from Launch Library
        elif command == "prevlaunch":
            await message.channel.send(fun.getPrevLaunch())
            # most recent launch
        elif command[:8] == "getevent":
            await message.channel.send(fun.getNameEvent(command[10:]))
            # get a specific launch from date
        elif command[:9] == "getlaunch":
            await message.channel.send(fun.getNameLaunch(command[10:]))
            # get a specific launch from name
        elif command == "starship":
            await message.channel.send(fun.getStarship())
            # get info on starship
        elif command == "nextevent":
            await message.channel.send(fun.getNextEvent())
            # get the next space event
        elif command == "prevevent":
            await message.channel.send(fun.getPrevEvent())
            # get the most recent space event
        else:
            await message.channel.send("I don't know that command. Please use `r!help` for a list of my commands.")

keep_alive()  
client.run(os.getenv('TOKEN'))