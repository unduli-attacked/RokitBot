# API access functions
import json
import requests
import os
import datetime
import pytz
import urllib.parse

def formatLaunchInfo(launchJson, launchDateTime):
    edtLaunch = launchDateTime.astimezone(pytz.timezone('US/Eastern'))
    mdtLaunch = launchDateTime.astimezone(pytz.timezone('US/Mountain'))
    pdtLaunch = launchDateTime.astimezone(pytz.timezone('US/Pacific'))
    dateString = "**Date:** NET {} UTC\n                    {} EDT\n                    {} MDT\n                    {} PDT\n".format(launchDateTime.strftime("%m-%d-%Y, %H:%M:%S"), edtLaunch.strftime("%m-%d-%Y, %H:%M:%S"), mdtLaunch.strftime("%m-%d-%Y, %H:%M:%S"), pdtLaunch.strftime("%m-%d-%Y, %H:%M:%S"))
    prettyString = ""
    if(launchJson['mission']==None):
        prettyString = ("**Mission Name:** {}\n"+"*Launched on:* {}\n*By:* {}\n*From:* {} in {}\n{}").format(launchJson["name"], launchJson["rocket"]["configuration"]["name"], launchJson["launch_service_provider"]["name"], launchJson["pad"]["name"], launchJson["pad"]["location"]["name"], dateString)
    else:
        prettyString = ("**Mission Name:** {}\n"+"*Launched on:* {}\n*To:* {}\n*By:* {}\n*From:* {} in {}\n{}").format(launchJson['mission']["name"], launchJson["rocket"]["configuration"]["name"], launchJson["mission"]["orbit"]["abbrev"], launchJson["launch_service_provider"]["name"], launchJson["pad"]["name"], launchJson["pad"]["location"]["name"], dateString)

    if(not (launchJson['probability']==None or launchJson['probability']==-1)):
        prettyString+= "**Launch Probability:** {}\n".format(launchJson['probability'])

    return prettyString

def getNextLaunch():
    response = requests.get("https://ll.thespacedevs.com/2.0.0/launch/upcoming/") # gets all upcoming launches
    jsonified = json.loads(response.text)
    nextLaunch = jsonified["results"][0] #first launch in the results array
    dateGood = False
    launchDateTime = datetime.datetime(2002, 1, 1)
    n = 0
    while not dateGood:
        nextLaunch = jsonified["results"][n] #first launch in the results array
        launchDate = nextLaunch["net"].split("T")[0]
        launchTime = nextLaunch["net"].split("T")[1][:8]

        launchDateTime = datetime.datetime(int(launchDate.split("-")[0]), int(launchDate.split("-")[1]), int(launchDate.split("-")[2]), hour=int(launchTime.split(":")[0]), minute=int(launchTime.split(":")[1]), second=int(launchTime.split(":")[2]), tzinfo = pytz.timezone('UTC'))

        n+=1
        dateGood = launchDateTime < datetime.datetime.now(tz=pytz.timezone('UTC'))

    return formatLaunchInfo(nextLaunch, launchDateTime)

def getPrevLaunch():
    response = requests.get("https://ll.thespacedevs.com/2.0.0/launch/previous/") # gets all upcoming launches
    jsonified = json.loads(response.text)
    prevLaunch = jsonified["results"][0] #first launch in the results array
    launchDate = prevLaunch["net"].split("T")[0]
    launchTime = prevLaunch["net"].split("T")[1][:8]

    launchDateTime = datetime.datetime(int(launchDate.split("-")[0]), int(launchDate.split("-")[1]), int(launchDate.split("-")[2]), hour=int(launchTime.split(":")[0]), minute=int(launchTime.split(":")[1]), second=int(launchTime.split(":")[2]), tzinfo = pytz.timezone('UTC'))

    return formatLaunchInfo(prevLaunch, launchDateTime)

def getNameLaunch(name):
    response = requests.get("https://ll.thespacedevs.com/2.0.0/launch/?search="+urllib.parse.quote(name)) # searches for launch
    jsonified = json.loads(response.text)
    if len(jsonified['results']) == 0:
        return "Not found."
    prevLaunch = jsonified["results"][0] #first launch in the results array
    launchDate = prevLaunch["net"].split("T")[0]
    launchTime = prevLaunch["net"].split("T")[1][:8]

    launchDateTime = datetime.datetime(int(launchDate.split("-")[0]), int(launchDate.split("-")[1]), int(launchDate.split("-")[2]), hour=int(launchTime.split(":")[0]), minute=int(launchTime.split(":")[1]), second=int(launchTime.split(":")[2]), tzinfo = pytz.timezone('UTC'))

    return formatLaunchInfo(prevLaunch, launchDateTime)

def formatEventInfo(event, eventDateTime):
    edtEvent = eventDateTime.astimezone(pytz.timezone('US/Eastern'))
    mdtEvent = eventDateTime.astimezone(pytz.timezone('US/Mountain'))
    pdtEvent = eventDateTime.astimezone(pytz.timezone('US/Pacific'))
    dateString = "**Date:** {} UTC\n            {} EDT\n            {} MDT\n            {} PDT\n".format(eventDateTime.strftime("%m-%d-%Y, %H:%M:%S"), edtEvent.strftime("%m-%d-%Y, %H:%M:%S"), mdtEvent.strftime("%m-%d-%Y, %H:%M:%S"), pdtEvent.strftime("%m-%d-%Y, %H:%M:%S"))

    prettyString = "**Event Name:** *{}*\n**Event Type:** {}\n**Description:** {}\n**Location:** {}\n{}".format(event['name'], event['type']['name'], event['description'], event['location'], dateString)

    if not event['video_url'] == None:
        prettyString += "**Watch Here:** {}".format(event['video_url']) #TODO figure out why tf hyperlinks aren't working

    return prettyString

def getNextEvent():
    response = requests.get("https://ll.thespacedevs.com/2.0.0/event/upcoming/") # gets all upcoming launches
    jsonified = json.loads(response.text)
    nextEvent = jsonified["results"][0] #first launch in the results array
    eventDate = nextEvent["date"].split("T")[0]
    eventTime = nextEvent["date"].split("T")[1][:8]

    eventDateTime = datetime.datetime(int(eventDate.split("-")[0]), int(eventDate.split("-")[1]), int(eventDate.split("-")[2]), hour=int(eventTime.split(":")[0]), minute=int(eventTime.split(":")[1]), second=int(eventTime.split(":")[2]), tzinfo = pytz.timezone('UTC'))

    return formatEventInfo(nextEvent, eventDateTime)

def getPrevEvent():
    response = requests.get("https://ll.thespacedevs.com/2.0.0/event/previous/") # gets all upcoming launches
    jsonified = json.loads(response.text)
    prevEvent = jsonified["results"][0] #first launch in the results array
    eventDate = prevEvent["date"].split("T")[0]
    eventTime = prevEvent["date"].split("T")[1][:8]

    eventDateTime = datetime.datetime(int(eventDate.split("-")[0]), int(eventDate.split("-")[1]), int(eventDate.split("-")[2]), hour=int(eventTime.split(":")[0]), minute=int(eventTime.split(":")[1]), second=int(eventTime.split(":")[2]), tzinfo = pytz.timezone('UTC'))

    return formatEventInfo(prevEvent, eventDateTime)

def getNameEvent(name):
    response = requests.get("https://ll.thespacedevs.com/2.0.0/event/?search="+urllib.parse.quote(name)) # gets all upcoming launches
    jsonified = json.loads(response.text)
    if len(jsonified['results']) == 0:
        return "Not found."
    nextEvent = jsonified["results"][0] #first launch in the results array
    eventDate = nextEvent["date"].split("T")[0]
    eventTime = nextEvent["date"].split("T")[1][:8]

    eventDateTime = datetime.datetime(int(eventDate.split("-")[0]), int(eventDate.split("-")[1]), int(eventDate.split("-")[2]), hour=int(eventTime.split(":")[0]), minute=int(eventTime.split(":")[1]), second=int(eventTime.split(":")[2]), tzinfo = pytz.timezone('UTC'))

    return formatEventInfo(nextEvent, eventDateTime)

def getStarship():
    return ""