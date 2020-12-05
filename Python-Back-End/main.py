import multiprocessing, time
from main_functions import MainFile, ReadJSON, updating_preferences, Path
from discordBot import DiscordBot as Bot_Discord


#To choose which platform to run on

def systemRun():
    system = ""
    while(system not in ["1", "2"]):
        print("______________________________\nWhich system are you running?\n\n1) Windows\n2) Ubuntu / Linux\n\nAnswer: ", end="")
        system = str(input())
        print("______________________________")
        
    if(system == "1"):
        system = "WIN"
    else:
        system = "LIN"
        
    Preferences_Path = Path("Storings\\preferences.json")
    PreFile = ReadJSON(Preferences_Path)
    PreFile["Preferences"]["System"] = system
    
    updating_preferences("System", system)

#main function
def main():
    mainProgram = multiprocessing.Process(target=MainFile)
    DiscordBot = multiprocessing.Process(target=Bot_Discord)
    
    print("\nIt's now running")
    
    DiscordBot.start()
    mainProgram.start()
    
    DiscordBot.join()
    mainProgram.join()

#MAIN PROGRAM

if __name__ == '__main__':
    systemRun()
    main()