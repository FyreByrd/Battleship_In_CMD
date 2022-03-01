#battleship.py: contains logic to run the game
#author: Aidan Jones

#<<<<<Import Statements>>>>>
from player import HumanPlayer
from board import Board
import os

#<<<<<Miscellaneous Variables, Classes, and Functions>>>>>
#--welcome message/logo
version_no = "2.0.0"
version = "_"*(15-len(version_no))+str(version_no)
welcome_string = """
 _________________________________________________________
     ____                                __                    
     /   )                  /          /    ) /     ,        
    /__ /    __  _/_  _/_  /   __      \     /__      ___ 
   /    )  /   ) /    /   /  /___)      \   /   ) /  /   )
  /____/  (___( (    (   /  (___    (____/ /   / /  /___/ 
                                                   /      
                                                  / 
 _____command_line________________________"""+version+"""_      
"""
#--clears the screen of the CLI
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')
#--contains methods to run the program
class BattleShipMain():
    #--method to get input
    def get_input(this, msg:str, case_sensitive=False, split=False, div=" "):
        try:
            inp = input(" "+msg+"> ")
        except (KeyboardInterrupt, EOFError):
            print("Program terminated by interrupt or end-of-file.")
            print("Exiting game . . .")
            exit()
        inp = str(inp)
        inp = inp.strip()
        if not case_sensitive:
            inp = inp.lower()
        return inp.split(div) if split else inp  
    #--constructor
    def __init__(this):
        pname = this.get_input("Type the name you would like to use ",case_sensitive=True)
        this.player = HumanPlayer(pname)
        this.opp = None
        print(" Welcome, "+str(this.player))
        print(" Type 'help' to list available commands")
    #--loop for running a game of Battleship
    def game_loop(this):
        #--setup
        initializing = True #loop flag variable
        initialized = False #check for if board is initialized
        ship_dict = this.player.get_board().shipdict.ships[0]
        msl = [ #master ship list
            "1: "+ship_dict[4]+"\n", #destroyer
            "2: "+ship_dict[3]+"\n", #submarine
            "3: "+ship_dict[2]+"\n", #cruiser
            "4: "+ship_dict[1]+"\n", #battleship
            "5: "+ship_dict[0]+"\n"  #aircraft carrier
        ]
        ship_string = msl[0]+msl[1]+msl[2]+msl[3]+msl[4]
        print(" Ship Placement:")
        print(this.player.get_board().ships())
        print(ship_string)
        while initializing:
            sel = this.get_input("",split=True)
            opt = sel[0]
            if opt == "help":
                print(" Ship Placement:")
                print(" help   - displays this message")
                print(" whoami - displays your username")
                print(" place  - places a ship")
                print("    usage:")
                print(" remove - removes a ship")
                print("    usage:")
                print(" reset  - clears all ships from the board")
                print(" random - randomizes the ship placement") 
                print(" play   - begins the game if the board is setup")               
                print(" clear  - unclogs the screen")
                print(" quit   - exits ship placement")
                print("")
            elif opt == "whoami":
                print(" username: "+str(this.player))
            elif opt == "place":
                #insert_ship
                print(this.player.get_board().ships())
                print(ship_string)
            elif opt == "remove":
                #remove_ship
                print(this.player.get_board().ships())
                print(ship_string)
            elif opt == "random":
                this.player.get_board().clear_board()
                this.player.get_board().randomize()
                initialized = True
                print(this.player.get_board().ships())
            elif opt == "reset":
                this.player.get_board().clear_board()
                initialized = False
                print(this.player.get_board().ships())
                print(ship_string)
            elif opt == "play":
                if initialized:
                    initializing = False
                else:
                    print(" You cannot play until all your ships are placed.")
            elif opt == "clear":
                clear_screen()
                print(this.player.get_board().ships())
                print(ship_string)
            elif opt == "quit":
                return "quit in ship placement"
            else:
                print(" Unrecognized command sequence:")
                print(" '"+" ".join(sel)+"'")
                print(" Use command 'help' for help")
        #--loop
        print("Starting game . . .")
    
    #--main loop function
    def main_loop(this):
        playing = True
        print(" Enter your desired command...")
        while playing:
            sel = this.get_input("",split=True)
            opt = sel[0]
            if opt == "help":
                print(" Main Menu:")
                print(" help   - displays this message")
                print(" whoami - displays your username")
                print(" new    - creates new game")
                #print("    usage:")
                #print("     -c - choose your setup [TBI]")
                #print("     -s - salvo mode")
                #print("     -a - advanced AI")
                #print(" test   - benchmarks the AI")
                #print("       options:")
                #print("     -a - advanced AI")
                #print("     -x - pits basic vs. advanced")
                print(" clear  - unclogs the screen")
                print(" quit   - exits the program")
                print("")
            elif opt == "whoami":
                print(" username: "+str(this.player))
            elif opt == "new":
                this.game_loop()
                print("Finished game . . .")
            elif opt == "clear":
                clear_screen()
            elif opt == "quit":
                playing = False
            else:
                print(" Unrecognized command sequence:")
                print(" '"+" ".join(sel)+"'")
                print(" Use command 'help' for help")

#--Main method
if __name__=="__main__":
    clear_screen()
    print(welcome_string)
    game = BattleShipMain()
    game.main_loop()
    