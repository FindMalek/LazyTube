import os, sys, json

import time, pytz
from pytz import timezone
from datetime import date, datetime, timedelta 


import googleapiclient.discovery

#get paths 
def Path(relativePath, systeme):
    if(systeme == 'LINUX'):
        return str(os.getcwd()) + "/" + relativePath
    elif(systeme == 'WIN'):
        return str(os.getcwd()) + "\\" + relativePath

#NEEDED PATHS
Logs_Path = Path("Storings\\logs.txt", 'WIN')
UploadedVideos_Path = Path("Storings\\UploadedVideos.json", 'WIN')
Preferences_Path = Path("Storings\\preferences.json", 'WIN')
DiscordBotPreferences_Path = Path("Storings\\DiscordBotPreferences.json", "WIN")


#delete this later we dont need it
def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))
   

#get the API key from the preferences.json file      
def GoogleAPI_Key():
    #addLog("(type=Function: GoogleAPI_Key) - Getting Google API Key [Not verified]")
    with open(Preferences_Path, 'r') as PrefFile:
        PreferencesFile = json.load(PrefFile)
    Google_API_Key = PreferencesFile["Preferences"]["Google API Key"]
    return Google_API_Key

#read any json file
def ReadJSON(path):
    with open(path, 'r') as file:
        return json.load(file)

#convert time to a more readable form for addLogs
def Convert_Time(time_complexe):
    return str(time_complexe)[:str(time_complexe).find('.')]

#Write all Logs in the log file
def addLog(action):
    with open(Logs_Path, 'a') as fileLog:
        fileLog.write(str(Logs_Time()) + ' > ' + action + '\n')
    with open(Logs_Path, 'r') as fileLog:
        fileLogs = fileLog.readlines()
        
    with open(Logs_Path, 'w') as fullFile:
        fullFile.write('')
        for line in fileLogs:
            fullFile.write(line)



#Time format for the AddLog function  
def Logs_Time():
    return '[ (' +  str(date.today()).replace('-', '/') + ')' + ' | ' + datetime.now().strftime("%A, %H:%M:%S")+']'

#Delay
def delay(prob_time):
    #addLog("(type=Delay) - " + str(prob_time))
    time.sleep(prob_time)


#Send the request for googleapiclient.discovery.build
def GoogleClientRequest(apiKey):
    #addLog('(type=Request: googleapiclient.discovery.build) - Checking for the avaibility of the API KEY')

    
    try:
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = apiKey)
    except Exception:
        #addLog("(type=Request: googleapiclient.discovery.build) - Google API Key isn't valid")   
        sys.exit("API KEY isn't valid for use.\nTry again!")
    
    #addLog('(type=Request: googleapiclient.discovery.build) - Got Google API Key [Verified]')
    delay(2.5)
    
    #addLog('(type=Youtube API) - Youtube Data API version 3')
    return youtube

#get delay intervales
def Preferences_Informations(option_chosen):
    if(option_chosen == "Delay before checking"):
        with open(Preferences_Path) as Preferences_File:
            PrefFile = json.load(Preferences_File)
        return PrefFile["Preferences"]["Delay before checking"]
    
    elif(option_chosen == "Delay before next checking loop starts"):
        with open(Preferences_Path) as Preferences_File:
            PrefFile = json.load(Preferences_File)
        return PrefFile["Preferences"]["Delay before next checking loop starts"]
    
    elif(option_chosen == "Latest loop run time"):
        with open(Preferences_Path) as Preferences_File:
            PrefFile = json.load(Preferences_File)
        return PrefFile["Preferences"]["Latest loop run time"]
    
    elif(option_chosen == "Number of loops"):
        with open(Preferences_Path) as Preferences_File:
            PrefFile = json.load(Preferences_File)
        return PrefFile["Preferences"]["Number of loops"]

    elif(option_chosen == "Intervale of upload"):
        with open(Preferences_Path) as Preferences_File:
            PrefFile = json.load(Preferences_File)
        return PrefFile["Preferences"]["Intervale of upload"]

#Get the API key + Time for the settings
def Base_Information(information_option):
    if(information_option == "Time = Start"):
        return datetime.now(pytz.timezone('Africa/Tunis')) - timedelta(0, Preferences_Informations("Delay before checking"))
    
    elif(information_option == "Time = Latest loop"):
        return Preferences_Informations("Latest loop run time")

#Getting informations updated in preferences.json
def updating_preferences(updating_option, data_option="", json_option=""):
    PrefFile = ReadJSON(Preferences_Path)
    
    if(updating_option == "Time = Start"):
        #addLog("(type=Function: updating_preferences, Time = Start) - Updated")
        PrefFile["Preferences"]["Latest loop run time"] = str(data_option)
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True)

    elif(updating_option == "Number of loops"):
        #addLog("(type=Function: updating_preferences, Number of loops) - Updated")
        PrefFile["Preferences"]["Number of loops"] = int(int(PrefFile["Preferences"]["Number of loops"]) + 1)
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True)
            
    elif(updating_option == "Latest check"):
        #addLog("(type=Function: updating_preferences, Latest check) - Updated")
        PrefFile["Channels"][json_option]["Latest check"] = str(data_option)
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True)
            
    elif(updating_option == "Quotas, Requests rate"):
        #addLog("(type=Function: updating_preferences, Quotas, Requests rate) - Updated")
        PrefFile["Preferences"]["Quotas"]["Requests rate"] = data_option
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True)
            
    elif(updating_option == "Quotas, Reset time"):
        #addLog("(type=Function: updating_preferences, Quotas, Reset time) - Updated")
        PrefFile["Preferences"]["Quotas"]["Reset time"] = str(data_option)
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True) 
            

#get the upload intervale and calculating it
def upload_intervale(Basic_Time_Now, channel):
    PrefFile = ReadJSON(Preferences_Path)["Channels"]

    if(PrefFile[channel]["Latest check"] == ""):
        AfterPublish = str(Basic_Time_Now).replace(" ", "T")
        BeforePublish = str(Basic_Time_Now + timedelta(0, Preferences_Informations("Intervale of upload"))).replace(" ", "T")
    else:
        AfterPublish = str(PrefFile[channel]["Latest check"]).replace(" ", "T")
        BeforePublish = str(datetime.strptime(PrefFile[channel]["Latest check"], "%Y-%m-%dT%H:%M:%S.%f%z") + timedelta(seconds = int(Preferences_Informations("Intervale of upload")))).replace(" ", "T")
        
    #addLog("(type=Function: upload_intervale) - BeforePublish: " + BeforePublish + ", AfterPublish: " + AfterPublish)
    return AfterPublish, BeforePublish

#getting contentDetails, snippet about a channel
def ChannelResponse_Activities(Channel, Youtube, AfterPublish, BeforePublish):
    Channel  = ReadJSON(Preferences_Path)["Channels"][Channel]
    ChannelID = Channel["Channel half-link"][Channel["Channel half-link"].find("/")+1:]
    #addLog("(type=Request: Youtube.activities) - Request of ChannelID: " + ChannelID)
    request = Youtube.activities().list(part="snippet,contentDetails",
                                        channelId=ChannelID,
                                        maxResults=1000,
                                        publishedAfter=AfterPublish,
                                        publishedBefore=BeforePublish)
    response = request.execute()
    
    #addLog("(type=Request: Youtube.activities) - Request of " + ChannelID + " Accepted")
    return response

#to get the thumbnail of the video for the discord bot
def ChannelResponse_Video(videoId, Youtube):
    #addLog("(type=Request: Youtube.activities) - Request of VideoID: " + videoId)
    request = Youtube.videos().list(
                            part="contentDetails,snippet",
                            id=videoId)
    response = request.execute()
    #addLog("(type=Request: Youtube.activities) - Request of VideoID: " + videoId + " Accepted")
    for item in response["items"]: 
        try:
            videoThumbnail = dict(dict(dict(dict(item).get("snippet")).get("thumbnails")).get("standard")).get("url")
            duration = item["contentDetails"]["duration"]
            return videoThumbnail, duration
        except Exception:
            pass
    

#check if the channel has passed the delay before checking (45 min)
def ChannelAvailibility(Channel, Basic_Time_Now):
    Channel  = ReadJSON(Preferences_Path)["Channels"][Channel]
    LatestCheck = datetime.strptime(Channel["Latest check"], "%Y-%m-%dT%H:%M:%S.%f%z")
    ChannelID = Channel["Channel half-link"][Channel["Channel half-link"].find("/")+1:]
    if(LatestCheck <= Basic_Time_Now):
        #addLog("(type=Function: ChannelAvailibility) - " + ChannelID + " Accepted")
        return True
    else:
        #addLog("(type=Function: ChannelAvailibility) - " + Channel + " Declined")
        return False

#get channelId of response
def getChannelId(channel, PreFile):
    return str(PreFile["Channels"][channel]["Channel half-link"])[PreFile["Channels"][channel]["Channel half-link"].find('/') + 1:]

#rate of requests
def QuotaCalculator(number):
    delay(1)
    PreFile = ReadJSON(Preferences_Path)
    time_now = datetime.now()
    ResetTime = datetime.strptime(PreFile["Preferences"]["Quotas"]["Reset time"], '%Y-%m-%d %H:%M:%S.%f')
    if(ResetTime >= (time_now - timedelta(hours=24))):
        if(PreFile["Preferences"]["Quotas"]["Requests rate"] >= 49700):
            #addLog("Requests rate has been exceeded (Paused for 24 hours)")
            time.sleep(60*60*24)
            updating_preferences("Quotas, Requests rate", 0)
    elif(ResetTime < (time_now - timedelta(hours=24))): 
        updating_preferences("Quotas, Reset time", time_now)
    updating_preferences("Quotas, Requests rate", PreFile["Preferences"]["Quotas"]["Requests rate"] + number)
    
    return PreFile["Preferences"]["Quotas"]["Requests rate"] + number


#NEXT UPDATE
#get channel color from their logo
#each channel gets its own constante colour
def ChannelColor():
    pass

#get the response and put every video details in a dictionary
def VideosAppender(response, Youtube, video_dict={}, channelId="" ):
    video_dict["Channel " +  str(channelId)] = []
    if(len(response["items"]) != 0):
        for items in response["items"]:
            videoId = str(dict(dict(items).get("contentDetails")).get("upload"))[str(dict(dict(items).get("contentDetails")).get("upload")).find(':') + 3: -2]
            if(videoId == ""):
                try:
                    videoId = dict(dict(dict(dict(items).get("contentDetails")).get("playlistItem")).get("resourceId"))[str(dict(dict(dict(dict(items).get("contentDetails")).get("playlistItem")).get("resourceId"))).find(':') + 3: -2]
                except Exception:
                    pass
            if(videoId != ""):    
                videoThumbnail_duration = ChannelResponse_Video(videoId, Youtube)
                videoThumbnail = videoThumbnail_duration[0]
                duration = videoThumbnail_duration[1]
                video_dict["Channel " +  str(channelId)].append({
                        "channelTitle": dict(dict(items).get("snippet")).get("channelTitle"),
                        "publishedAt": dict(dict(items).get("snippet")).get("publishedAt"),
                        "title": dict(dict(items).get("snippet")).get("title"),
                        "videoId": videoId,
                        "discordMessage": "False",
                        "duration" : duration,
                        "images": {
                            "videoThumbnail": videoThumbnail,
                            "channelLogo": "Null" #its None
                        }
                        })
            #addLog("(type=Function: VideosAppender) - Added " + videoId)
    return video_dict

#add the video_dict to .json file "UploadedVideos"
def Add_Uploaded_Contenent(videos_dict):
    #addLog("(type=Update) - Updating UploadedVideos.json")
    with open(UploadedVideos_Path, "w") as write_file:
        json.dump(videos_dict, write_file, indent=4, sort_keys=True)
    #addLog("(type=Update) - Updated UploadedVideos.json")

#main filee"
#add logs just for setup

def MainFile():
    x=0
    Google_API_Key = GoogleAPI_Key() #Get API key from the data base
    Youtube = GoogleClientRequest(Google_API_Key) #Send a request to use the API key in YOUTUBE DATA V3
    
    Basic_Time = Base_Information("Time = Start") #get time to check from
    #addLog("(loop=" + str(Preferences_Informations("Number of loops")) + ") Youtube checking time: "+ str(Convert_Time(Basic_Time))) #logs
    updating_preferences("Time = Start", Basic_Time) #update the data base 
    updating_preferences("Number of loops") #update the data base 
    
    videos_dict = {}
    while(x != 1):
        PreFile = ReadJSON(Preferences_Path) #get database
        for channel in PreFile["Channels"]: #get through every channel to check for videos
            
            # AfterPublish = upload_intervale(Basic_Time, channel)[0]
            # BeforePublish = upload_intervale(Basic_Time, channel)[1]
            # AfterPublish = "2020-10-26T22:37:21.220816+01:00"
            
            AfterPublish = "2020-11-20T22:37:21.220816+01:00" #get period to check from AfterPublish
            BeforePublish = str(Basic_Time).replace(" ", "T") #get period to check from BeforePublish
            
            if(ChannelAvailibility(channel, Basic_Time)): #check if the channel is ready to be checked
                response = ChannelResponse_Activities(channel, Youtube, AfterPublish, BeforePublish) #response of the activities of the channel
                updating_preferences("Latest check", BeforePublish, channel) #update the channel latest check
                videos_dict = VideosAppender(response, Youtube, videos_dict, getChannelId(channel, PreFile)) # add video list of that channel to the list/dict
                QuotaCalculator(2)
        x = 1
                
        Add_Uploaded_Contenent(videos_dict) #put the list/dict in the uploaded videos




MainFile()