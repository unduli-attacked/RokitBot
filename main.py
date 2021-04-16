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
            ["futureLaunch [index]", "Sends data on a future launch. Index 0 is the soonest launch, index 1 is the launch after that, etc."],
            ["prevLaunch", "Sends data on the most recent rocket launch."],
            ["pastLaunch [index]", "Sends data on a past launch. Index 0 is the most recent launch, index 1 is the launch before that, etc."],
            ["getLaunch [keyword]", "Searches for a launch and returns data if found."],
            ["nextEvent", "Sends data on the next space event."],
            ["futureEvent [index]", "Sends data on a future event. Index 0 is the soonest event, index 1 is the event after that, etc."],
            ["prevEvent", "Sends data on the most recent space event."],
            ["pastEvent [index]", "Sends data on a past event. Index 0 is the most recent event, index 1 is the event before that, etc."],
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
        elif command[:12] == "futurelaunch":
            if len(command) > 13 and command[13:].isdigit():
                await message.channel.send(fun.getNextLaunch(pos=int(command[13:])))
            else:
                embed = discord.Embed()
                embed.description = "{} is an invalid value.".format(command[13:])
                await message.channel.send(embed=embed)
        elif command == "prevlaunch":
            await message.channel.send(fun.getPrevLaunch())
            # most recent launch
        elif command[:10] == "pastlaunch":
            if len(command) > 11 and command[11:].isdigit():
                await message.channel.send(fun.getPrevLaunch(pos=int(command[11:])))
            else:
                embed = discord.Embed()
                embed.description = "{} is an invalid value.".format(command[11:])
                await message.channel.send(embed=embed)
        elif command[:8] == "getevent":
            event = fun.getNameEvent(command[10:])
            await message.channel.send(event[0])
            embed = discord.Embed()
            embed.description = "Watch the event [here]({}).".format(event[1])
            await message.channel.send(embed=embed)
            # get a specific launch from date
        elif command[:9] == "getlaunch":
            await message.channel.send(fun.getNameLaunch(command[10:]))
            # get a specific launch from name
        elif command == "starship":
            await message.channel.send(fun.getStarship())
            # get info on starship
        elif command == "nextevent":
            event = fun.getNextEvent()
            await message.channel.send(event[0])
            embed = discord.Embed()
            embed.description = "Watch the event [here]({}).".format(event[1])
            await message.channel.send(embed=embed)
            # get the next space event
        elif command[:11] == "futureevent":
            if len(command) > 12 and command[12:].isdigit():
                await message.channel.send(fun.getNextEvent(pos=int(command[12:])))
            else:
                embed = discord.Embed()
                embed.description = "{} is an invalid value.".format(command[12:])
                await message.channel.send(embed=embed)
        elif command == "prevevent":
            event = fun.getPrevEvent()
            await message.channel.send(event[0])
            embed = discord.Embed()
            embed.description = "Watch the event [here]({}).".format(event[1])
            await message.channel.send(embed=embed)
            # get the most recent space event
        elif command[:9] == "pastevent":
            if len(command) > 10 and command[10:].isdigit():
                await message.channel.send(fun.getNextLaunch(pos=int(command[10:])))
            else:
                embed = discord.Embed()
                embed.description = "{} is an invalid value.".format(command[10:])
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.description = "I don't know that command. Please use `r!help` for a list of my commands."
            await message.channel.send(embed=embed)

keep_alive()  
client.run(os.getenv('TOKEN'))