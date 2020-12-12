import os, sys, json

import time, pytz
from pytz import timezone
from datetime import date, datetime, timedelta 

import googleapiclient.discovery




#read any json file
def ReadJSON(path):
    with open(path, 'r') as file:
        return json.load(file)

#Needed for the path function
def TranslatePaths(path):
    operator = "\\"
    if(operator in path):
        folderName = path[:path.find("\\")]
        fileName = path[path.find("\\") + 1:]
        return "/" + folderName + "/" +  fileName
    else:
        fileName = path[path.find("\\") + 1:]
        return  "/" + fileName
     
#get paths 
def Path(relativePath=""):
    try: 
        Prefile = ReadJSON("Storings\preferences.json")
    except Exception:
        pass
    else:
        Prefile = ReadJSON("Storings/preferences.json")
        
    systeme = Prefile["Preferences"]["System"]
    
    if(systeme == 'LIN'):
        return str(os.getcwd()) + "/" + TranslatePaths(relativePath)
    elif(systeme == 'WIN'):
        return str(os.getcwd()) + "\\" + relativePath
    
    
#NEEDED PATHS
Logs_Path = Path("Storings\\logs.txt")
UploadedVideos_Path = Path("Storings\\UploadedVideos.json")
Preferences_Path = Path("Storings\\preferences.json")
DiscordBotPreferences_Path = Path("Storings\\DiscordBotPreferences.json")


#get the API key from the preferences.json file      
def GoogleAPI_Key():
    #addLog("(type=Function: GoogleAPI_Key) - Getting Google API Key [Not verified]")
    with open(Preferences_Path, 'r') as PrefFile:
        PreferencesFile = json.load(PrefFile)
    Google_API_Key = PreferencesFile["Preferences"]["Google API Key"]
    return Google_API_Key

#convert time to a more readable form for addLogs
def Convert_Time(time_complexe):
    return str(time_complexe)[:str(time_complexe).find('.')]
            
#logs
def Log(string_log):
    if(string_log == "Setup"):
        Message = ['=====================================================\n', '[LazyTube] log file\n', 'Â© Malek Gara-Hellal\n', '=====================================================\n']
        with open(Logs_Path, 'w') as fileLog:
                fileLog.write("")
        for line in Message:
            with open(Logs_Path, 'a') as fileLog:
                fileLog.write(line)
                
    elif(string_log == "Done"):
        pass
    
    else:
        with open(Logs_Path, 'a') as fileLog:
            fileLog.write(Logs_Time() + " " + string_log + "\n")

#Time format for the AddLog function  
def Logs_Time():
    dates = str(date.today())
    times = datetime.strftime(datetime.now(), "%I:%M:%S %p")
    return '[' +  dates + ' | ' + times + ']'

#Delay
def delay(prob_time):
    #addLog("(type=Delay) - " + str(prob_time))
    time.sleep(prob_time)

#Send the request for googleapiclient.discovery.build
def GoogleClientRequest(apiKey):
    Log("(type=Request: googleapiclient.discovery.build) - Checking for the avaibility of the API KEY")
    try:
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = apiKey)
    except Exception:
        Log("(type=Request: googleapiclient.discovery.build, Youtube v3) - API Key ERROR")
        sys.exit("API KEY isn't valid for use.\nTry again!")
    
    Log("(type=Request: googleapiclient.discovery.build, Youtube v3) - Valid API Key")
    delay(2.5)
    Log('(type=Youtube API) - Youtube Data API version 3')
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
        PrefFile["Preferences"]["Latest loop run time"] = str(data_option)
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True)

    elif(updating_option == "Number of loops"):
        PrefFile["Preferences"]["Number of loops"] = int(int(PrefFile["Preferences"]["Number of loops"]) + 1)
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True)
            
    elif(updating_option == "Latest check"):
        PrefFile["Channels"][json_option]["Latest check"] = str(data_option)
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True)
            
    elif(updating_option == "Quotas, Requests rate"):
        PrefFile["Preferences"]["Quotas"]["Requests rate"] = data_option
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True)
            
    elif(updating_option == "Quotas, Reset time"):
        PrefFile["Preferences"]["Quotas"]["Reset time"] = str(data_option)
        with open(Preferences_Path, 'w') as Preferences_File:
            json.dump(PrefFile, Preferences_File, indent=4, sort_keys=True) 
    
    elif(updating_option == "System"):
        PrefFile["Preferences"]["System"] = data_option
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
        
    return AfterPublish, BeforePublish

#getting contentDetails, snippet about a channel
def ChannelResponse_Activities(Channel, Youtube, AfterPublish, BeforePublish):
    Channel  = ReadJSON(Preferences_Path)["Channels"][Channel]
    ChannelID = Channel["Channel half-link"][Channel["Channel half-link"].find("/")+1:]
    request = Youtube.activities().list(part="snippet,contentDetails",
                                        channelId=ChannelID,
                                        maxResults=1000,
                                        publishedAfter=AfterPublish,
                                        publishedBefore=BeforePublish)
    response = request.execute()
    
    return response

#to get the thumbnail of the video for the discord bot
def ChannelResponse_Video(videoId, Youtube):
    request = Youtube.videos().list(
                            part="contentDetails,snippet",
                            id=videoId)
    response = request.execute()
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
        return True
    else:
        return False

#get channelId of response
def getChannelId(channel, PreFile):
    return str(PreFile["Channels"][channel]["Channel half-link"])[PreFile["Channels"][channel]["Channel half-link"].find('/') + 1:]

#rate of requests
def QuotaCalculator(number):
    delay(1)
    PreFile = ReadJSON(Preferences_Path)
    updating_preferences("Quotas, Requests rate", PreFile["Preferences"]["Quotas"]["Requests rate"] + number)
    time_now = datetime.now()
    ResetTime = datetime.strptime(PreFile["Preferences"]["Quotas"]["Reset time"], '%Y-%m-%d %H:%M:%S.%f')
    if(ResetTime >= (time_now - timedelta(hours=24))):
        if(PreFile["Preferences"]["Quotas"]["Requests rate"] >= 49700):
            Log("Requests rate has been exceeded (Paused for 24 hours)")
            time.sleep(60*60*24)
            Log("Requests rate has been reset!")
            updating_preferences("Quotas, Requests rate", 0)
            
    if(ResetTime < (time_now - timedelta(hours=24))): 
        updating_preferences("Quotas, Requests rate", 0)
        Log("Requests rate has been reset!")
        updating_preferences("Quotas, Reset time", time_now)
    


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
    return video_dict

#add the video_dict to .json file "UploadedVideos"
def Add_Uploaded_Contenent(videos_dict):
    Uploadfile = ReadJSON(UploadedVideos_Path)
    Uploadfile.update(videos_dict)
        
    with open(UploadedVideos_Path, "w") as write_file:
        json.dump(Uploadfile, write_file, indent=4, sort_keys=True)

#main filee"
#add logs just for setup

def MainFile():
    Google_API_Key = GoogleAPI_Key() #Get API key from the data base
    Log("Setup")
    Youtube = GoogleClientRequest(Google_API_Key) #Send a request to use the API key in YOUTUBE DATA V3
    Basic_Time = Base_Information("Time = Start") #get time to check from
    updating_preferences("Time = Start", Basic_Time) #update the data base 
    updating_preferences("Number of loops") #update the data base 
    
    while(True):
        PreFile = ReadJSON(Preferences_Path) #get database
        videos_dict = {}
        for channel in PreFile["Channels"]: #get through every channel to check for videos
            
            AfterPublish = upload_intervale(Basic_Time, channel)[0]
            BeforePublish = upload_intervale(Basic_Time, channel)[1]
            if(channel == "Channel UC0fiLCwTmAukotCXYnqfj0A"):
                print("=======================")
                print("AfterPublish: ",  AfterPublish, "BeforePublish: ", BeforePublish)
                print(channel)
                print("=======================")
            # AfterPublish = "2020-10-26T22:37:21.220816+01:00"
            
            if(ChannelAvailibility(channel, Basic_Time)): #check if the channel is ready to be checked
                response = ChannelResponse_Activities(channel, Youtube, AfterPublish, BeforePublish) #response of the activities of the channel
                updating_preferences("Latest check", BeforePublish, channel) #update the channel latest check
                videos_dict = VideosAppender(response, Youtube, videos_dict, getChannelId(channel, PreFile)) # add video list of that channel to the list/dict
                QuotaCalculator(2)
                
        Add_Uploaded_Contenent(videos_dict) #put the list/dict in the uploaded videos
