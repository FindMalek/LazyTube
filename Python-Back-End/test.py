from main_functions import addLog, delay, GoogleAPI_Key, Path, Base_Information, Preferences_Informations
from main_functions import updating_preferences, ReadJSON, upload_intervale, ChannelResponse, ChannelAvailibility
from main_functions import GoogleClientRequest, VideosAppender, pretty, ReadJSON
import os, sys, json, time

import discord
from discord.ext import commands, tasks
from itertools import cycle

from pytz import timezone
import pytz

from datetime import date, datetime, timedelta 
import googleapiclient.discovery

##NEEDED PATHS
Logs_Path = Path("Storings\\logs.txt", 'WIN')
UploadedVideos_Path = Path("Storings\\UploadedVideos.json", 'WIN')
Preferences_Path = Path("Storings\\preferences.json", 'WIN')

from discordBot import ChannelIds
from discordBot import Preferences_Informations as Preferences_Informations_BOT
   
def PrepareMessages(videos_dict, channels_keys):
    list = []
    videoIds = []
    for channel_key in channels_keys:
        videos_list = videos_dict[channel_key]
        
        for video_in_channel in videos_list:
            if(video_in_channel["discordMessage"] == "False"):
                #Video must be sent
                ChannelName = video_in_channel["channelTitle"]
                PublishTime = video_in_channel["publishedAt"] #Change the format to make it more readable
                VideoTitle = video_in_channel["title"]
                VideoLink = "https://www.youtube.com/watch?v=" + video_in_channel["videoId"]
                ChannelId = channel_key[channel_key.find(" ") + 1:]
                
                VideoDict = {
                    "ChannelName": ChannelName,
                    "PublishTime": PublishTime,
                    "VideoTitle": VideoTitle,
                    "VideoLink": VideoLink,
                    "ChannelId": ChannelId
                    }
                list.append(VideoDict)
                videoIds.append(video_in_channel["videoId"])
    return list
   
def SendMessage_Discord(videos_list):
    #do the emoji react to do actions
    #do the embed
    # "ChannelName": ChannelName,
    # "PublishTime": PublishTime,
    # "VideoTitle": VideoTitle,
    # "VideoLink": VideoLink,
    # "ChannelId": ChannelId
                      
    for video_informations in videos_list:
        pass
    pass


client = commands.Bot(case_insensitive=True, command_prefix='/')
    
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Do /help'))
    send_discord_message.start() #to start the task.loop function
        
    await client.get_channel(Preferences_Informations_BOT("Channel Id")).send('---------------\n\n\n**Rise and Shine LazyTube,  '+ '<@321378241040482304>' +'**\n\n\n---------------')


@tasks.loop(seconds=int(Preferences_Informations_BOT("Function interval checking")))
async def send_discord_message():
    UploadedVideos = dict(ReadJSON(UploadedVideos_Path))
    ChannelIds_list = ChannelIds(UploadedVideos, "Channels")
    VideosList = PrepareMessages(UploadedVideos, ChannelIds_list)
            
    SendMessage_Discord(VideosList)


@client.command(aliases = ['on'])
async def on_check(ctx):   
    await ctx.send("I'm online and working!")
    
client.run(Preferences_Informations_BOT("Discord API Key"))