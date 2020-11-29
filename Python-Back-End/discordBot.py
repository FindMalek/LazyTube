import os, time, asyncio, json, re

import discord
from discord.ext import commands, tasks
from itertools import cycle

from main_functions import Logs_Time, addLog, Path, delay, ReadJSON



#get values from DiscordBotPreferences_Path
def Preferences_Informations(option_chosen):
    preferences = ReadJSON(DiscordBotPreferences_Path)
    
    if(option_chosen == "Channel Id"):
        return preferences["Configurations"]["Channel Id"]
    elif(option_chosen == "Function interval checking"):
        return preferences["Configurations"]["Function interval checking"]
    elif(option_chosen == "Discord API Key"):
        return preferences["Configurations"]["Discord API Key"]

#gets channel ids or channel keys
def ChannelIds(UploadedVideos, option_chosen):
    if(option_chosen == "Ids"):
        channels = []
        for channel in UploadedVideos.keys():
            channels.append(channel[channel.find(' ') + 1:])
        return channels
    
    elif(option_chosen == "Channels"):
        return UploadedVideos.keys()

#makes the time more readable
def durationBeautifier(duration):
    hours = hours_patter.search(duration)
    minutes = minutes_patter.search(duration)
    seconds = seconds_pattern.search(duration)

    minutes = minutes.group(1) if minutes else "00"
    seconds = seconds.group(1) if seconds else "00"
    hours = hours.group(1) if hours else ""
    if(hours != ""):
        hours += ":"
        
    return str(hours)+str(minutes).zfill(2)+":"+str(seconds).zfill(2)

#makes the upload time more readable
def TimeBeautifier(times):
    return str(times)[:str(times).find("T")] + " " + str(times)[str(times).find("T") + 1:-4]

#write the json file in a beautiful manner
def Write_UploadedVideos(dictionary):
    with open(UploadedVideos_Path, "w") as write_file:
        json.dump(dictionary, write_file, indent=4, sort_keys=True)

#i really forgot
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
                videoThumbnail = video_in_channel["images"]["videoThumbnail"]
                VideoLink = "https://www.youtube.com/watch?v=" + video_in_channel["videoId"]
                ChannelId = channel_key[channel_key.find(" ") + 1:]
                duration = video_in_channel["duration"]
                
                VideoDict = {
                    "ChannelName": ChannelName,
                    "PublishTime": PublishTime,
                    "VideoTitle": VideoTitle,
                    "VideoLink": VideoLink,
                    "ChannelId": ChannelId,
                    "channelLogo": "Null",
                    "videoThumbnail": videoThumbnail,
                    "duration": durationBeautifier(duration)
                    }
                list.append(VideoDict)
                videoIds.append(video_in_channel["videoId"])

    for channel_key in channels_keys:
        length_channel = len(videos_dict[channel_key])
        for i in range(0, length_channel):
            if(videos_dict[channel_key][i]["videoId"] in videoIds):
                videos_dict[channel_key][i]["discordMessage"] = "True"
    Write_UploadedVideos(videos_dict)
    
    return list
  
#default settings
#MAKE SURE TO USE THE PICTURE COLOR CHOOSING IN THE V3 VERSION
def EmbedSetting(title="", description=""):
    embed = discord.Embed(
        title = title,
        descreption = description,
        colour = discord.Colour.blue())
    return embed

#make the masked links in the channelname as well as videotitle for videolink
#MAKE THE REACTS FUNCTIONAL IN THIS VERSION  
def message_beautifier(video_informations, videoThumbnail, ChannelLink):
    ChannelName = video_informations["ChannelName"]
    PublishTime = video_informations["PublishTime"]
    VideoTitle = video_informations["VideoTitle"]
    channelLogo = video_informations["channelLogo"] #find a solution
    VideoLink = video_informations["VideoLink"]
    duration = video_informations["duration"]
    
    embed = EmbedSetting(VideoTitle, "Description")
    embed.set_footer(text = TimeBeautifier(PublishTime))
    embed.set_image(url=videoThumbnail)
    embed.set_author(name=ChannelName, icon_url="https://images.pexels.com/photos/5020995/pexels-photo-5020995.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500")
    embed.add_field(name=VideoLink, value="*" + str(duration) +"*")
    return embed      


#main function of discord bot
def DiscordBot():
    client = commands.Bot(case_insensitive=True, command_prefix='/')
    
    #turn on the bot
    @client.event
    async def on_ready():
        #addLog(g('(run=DiscordBot) Bot is getting ready for duty...')
        await client.change_presence(activity=discord.Game(name='Do /help'))
        send_discord_message.start() #to start the task.loop function
        #addLog(g('(run=DiscordBot) Bot is ready')
        
        await client.get_channel(Preferences_Informations("Channel Id")).send('---------------\n\n\n**Rise and Shine LazyTube,  '+ '<@321378241040482304>' +'**\n\n\n---------------')

    #keep sending "FALSE" valued videos
    @tasks.loop(seconds=int(Preferences_Informations("Function interval checking")))
    async def send_discord_message():
        channel = client.get_channel(int(Preferences_Informations("Channel Id")))
        
        UploadedVideos = dict(ReadJSON(UploadedVideos_Path))
        ChannelIds_list = ChannelIds(UploadedVideos, "Channels")
        VideosList = PrepareMessages(UploadedVideos, ChannelIds_list)
        
        

        for video_informations in VideosList:

            ChannelLink = "https://www.youtube.com/channel/" + video_informations["ChannelId"]
            videoThumbnail = video_informations["videoThumbnail"]
            await channel.send(embed=message_beautifier(video_informations, videoThumbnail, ChannelLink))
            
    #set default sending channel   
    @client.command(aliases = ['set'])
    async def set_default_channel(ctx):
        print(ctx)
    
    #check if the bot is on 
    @client.command(aliases = ['on'])
    async def on_check(ctx):   
        await ctx.send("I'm online and working!")
    
    #add a function to add channel and make sure they exist
    
    client.run(Preferences_Informations("Discord API Key"))
        
#NEEDED PATHS
Logs_Path = Path("Storings\\logs.txt", "WIN")
UploadedVideos_Path = Path("Storings\\UploadedVideos.json", "WIN")
Preferences_Path = Path("Storings\\preferences.json", "WIN")
DiscordBotPreferences_Path = Path("Storings\\DiscordBotPreferences.json", "WIN")

#NEEDED Variables
minutes_patter = re.compile(r"(\d+)M")
hours_patter = re.compile(r"(\d+)H")
seconds_pattern = re.compile(r"(\d+)S")

DiscordBot()