import multiprocessing 
from main_functions import MainFile, systemRun
from discordBot import DiscordBot as Bot_Discord

def main():
    systemRun()
    
    mainProgram = multiprocessing.Process(target=MainFile)
    DiscordBot = multiprocessing.Process(target=Bot_Discord)
        
    DiscordBot.start()
    mainProgram.start()

    DiscordBot.join()
    mainProgram.join()


#MAIN PROGRAM
if __name__ == '__main__':
    main()