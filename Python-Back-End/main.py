import multiprocessing 
from main_functions import MainFile
from discordBot import sendMessage

def main():
    mainProgram = multiprocessing.Process(target=MainFile)
    sendingDiscordMessage = multiprocessing.Process(target=sendMessage)
        
    sendingDiscordMessage.start()
    mainProgram.start()

    sendingDiscordMessage.join()
    mainProgram.join()


#MAIN PROGRAM
if __name__ == '__main__':
    main()