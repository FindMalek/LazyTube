import json
import os
from main_functions import Path

#NEEDED PATHS
Logs_Path = Path("Storings\\logs.txt", 'WIN')
UploadedVideos_Path = Path("Storings\\UploadedVideos.json", 'WIN')
Preferences_Path = Path("Storings\\preferences.json", 'WIN')
DiscordBotPreferences_Path = Path("Storings\\DiscordBotPreferences.json", "WIN")


def Setup_Preferences(pathprefernces):
    with open(pathprefernces, "r") as Data_File:
        data = json.load(Data_File)
        
    data['Preferences'] = {"Google API Key": 'AIzaSyAM3YG7QAGmwiz36vKksbalOwKFKGisxVk',
                           "Delay before checking": 2700,
                           "Delay before next checking loop starts": 3600 ,
                           "Intervale of upload": 1200,
                           "Latest loop run time" : "",
                           "Number of loops" : 0,
                           "Liked artists" : ["shyler", "soap", "rivilin", "sepha", "big roshi"],
                           "Disliked artists" : ["sewerperson", "$uicideboy$"]
                           }
    #data['Channels'] = {}


    
    with open(pathprefernces, "w") as write_file:
        json.dump(data, write_file, indent=4, sort_keys=True)
    return data

def Artists(text):
    answer, list, counter = "", [], 1
    while(answer != "."):
        answer = input(text + " ("+ str(counter) + "): ")
        counter += 1
        if(answer != "."):
            list.append(answer)
    return list

def settingup_pref(pathprefernces):
    with open(pathprefernces, "r") as Data_File:
        DataFile = json.load(Data_File)
    try:
        DataFile["Preferences"]
    except Exception:
        data = {}
        data['Channels'] = {}
        googleapikey = input("Google API Key: ")
        delaybeforechecking = int(input("Delay before checking: "))
        delaybeforestart = int(input("Delay before next checking loop starts: "))
        intervaleofupload = int(input("Intervale of upload"))
        likedartists = Artists("Liked artist")
        dislikedartists = Artists("Disliked artist")
        
        data['Preferences'] = {"Google API Key": googleapikey,
                            "Delay before checking": delaybeforechecking,
                            "Delay before next checking loop starts": delaybeforestart,
                            "Intervale of upload": intervaleofupload,
                            "Liked artists" : likedartists,
                            "Disliked artists" : dislikedartists
                            }
        with open(pathprefernces, "w") as write_file:
            json.dump(data, write_file, indent=4, sort_keys=True)

def Setup_DiscordPreferences(DiscordBotPreferences_Path):
    data = {}
    data["Configurations"] = {}
    data["Discord API Key"] = "NzU0NzI5NDc2NTAzNTAyOTUw.X14-mQ.DOvVBS5R4Z2kgmnU9nHVoVrLUpk"
    data["Configurations"] = {
        "Function interval checking": 2.15,
        "Channel Id": 763846453516566560
    }
    with open(DiscordBotPreferences_Path, "w") as write_file:
        json.dump(data, write_file, indent=4, sort_keys=True)
        
Setup_DiscordPreferences(DiscordBotPreferences_Path)