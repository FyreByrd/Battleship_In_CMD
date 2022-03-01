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
    #--converts a string to a coordinate
    def str2coord(this, s:str):
        if len(s) < 2:
            raise ValueError
        return (str(s[0]),int(s[1:]) -1)
    #--loop for running a game of Battleship
    def game_loop(this):
        #--setup
        initializing = True #loop flag variable
        initialized = False #check for if board is initialized
        ship_dict = this.player.get_board().shipdict.ships[0]
        msl = [ #master ship list
            "1: "+ship_dict[4], #destroyer
            "2: "+ship_dict[3], #submarine
            "3: "+ship_dict[2], #cruiser
            "4: "+ship_dict[1], #battleship
            "5: "+ship_dict[0]  #aircraft carrier
        ]
        ship_string = msl[0]+"\n"+msl[1]+"\n"+msl[2]+"\n"+msl[3]+"\n"+msl[4]
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
                print(" board  - prints the board and ship availability")
                print(" place  - places a ship")
                print("    usage:")
                print("          ship  coordinate  rotation")
                print("    place [1-5] [a-j][1-10] [0-1]")
                print("    example:")
                print("    place 5 g4 1")
                print(" remove - removes a ship")
                print("    usage:")
                print("           coordinate")
                print("    remove [a-j][1-10]")
                print("    example:")
                print("    remove g4")
                print(" reset  - clears all ships from the board")
                print(" random - randomizes the ship placement") 
                print(" play   - begins the game if the board is setup")               
                print(" clear  - unclogs the screen")
                print(" quit   - exits ship placement")
                print("")
            elif opt == "whoami":
                print(" username: "+str(this.player))
            elif opt == "board":
                print(this.player.get_board().ships())
                print(ship_string)
            elif opt == "place":
                if len(sel) < 4:
                    print(" too few options specified")
                    continue
                s = sel[1] #ship
                try:
                    c = this.str2coord(sel[2]) #coordinate
                except ValueError:
                    print(" Invalid coordinates")
                    continue
                #build list of indices for menu check
                s_arr = ship_string.split("\n")
                arr_inds = []
                for i in range(len(s_arr)):
                    if s_arr[i] != "":
                        arr_inds.append(s_arr[i][0])
                if s not in arr_inds:
                    print(" "+s+" is not a valid selection")  
                    continue  
                #inserts ship
                try:
                    i = this.player.get_board().conv2int(c)
                except ValueError:
                    print(" invalid coordinates")
                    continue
                b = this.player.get_board().insert_ship(i, int(sel[3])%2, 5-int(s), s)
                if not b:
                    print(" ship could not be placed at "+sel[2])
                else:
                    #updates ship menu
                    ship_string = ""
                    for i in range(len(arr_inds)):
                        if s_arr[i][0] != s:
                            ship_string += s_arr[i]+"\n"
                if len(ship_string) == 0:
                    initialized = True
                print(this.player.get_board().ships())
                print(ship_string)
            elif opt == "remove":
                if len(sel) < 2:
                    print(" too few options specified")
                    continue
                try:
                    c = this.str2coord(sel[1]) #coordinate
                except ValueError:
                    print(" Invalid coordinates")
                    continue
                ch = this.player.get_board().dat2char(this.player.get_board().conv2int(c),"raw")
                if ch not in "12345":
                    print(" There is no ship at "+sel[1]+" to remove")
                    continue
                #removes ship
                s = this.player.get_board().remove_ship(ch)
                #rebuilds menu
                s_arr = ship_string.split("\n")
                print(s_arr)
                ship_string = ""
                arr_inds  = []
                for st in s_arr:
                    if st != "":
                        arr_inds.append(st[0])
                arr_inds.append(ch)
                arr_inds.sort()
                for i in arr_inds:
                    ship_string += msl[int(i)-1]+"\n"
                
                print(this.player.get_board().ships())
                print(ship_string)
                initialized = False
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
        print("gameplay not implemented yet")
    
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
                print("In main menu")
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
    