#battleship.py: contains logic to run the game
#author: Aidan Jones

#<<<<<Import Statements>>>>>
from player import HumanPlayer, StupidAI, BasicAI, AdvancedAI, WebPlayer
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
    def get_input(this, msg:str="", case_sensitive=False, split=False, div=" "):
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
        #ship menu      destroyer            submarine             cruiser               battleship            aircraft carrier
        ship_string = " 1: "+ship_dict[4]+"\n 2: "+ship_dict[3]+"\n 3: "+ship_dict[2]+"\n 4: "+ship_dict[1]+"\n 5: "+ship_dict[0]
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
                #check if s is an int
                try:
                    tmp = int(s)
                except ValueError:
                    print(" "+s+" is not a valid selection")
                    continue
                #get coordinates
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
                        arr_inds.append(s_arr[i][1])
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
                    i = ship_string.index(s)
                    ship_string = ship_string[:i]+"X"+ship_string[i+1:]
                #checks to see if all ships have been placed
                initialized = True
                for n in "12345":
                    if n in ship_string:
                        initialized = False
                        break
                #prints view
                print(this.player.get_board().ships())
                print(ship_string)
                if initialized:
                    print(" All ships have been placed.")
            elif opt == "remove":
                #initial error checking
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
                i = ship_string.index(s[9:])
                ship_string = ship_string[:i-3]+ch+ship_string[i-2:]
                #prints view
                print(this.player.get_board().ships())
                print(ship_string)
                print(" "+s+" at "+sel[1])
                initialized = False
            elif opt == "random":
                this.player.get_board().clear_board()
                this.player.get_board().randomize()
                initialized = True
                #rebuilds menu
                for n in "12345":
                    try:
                        i = ship_string.index(n)
                        ship_string = ship_string[:i]+"X"+ship_string[i+1:]
                    except ValueError:
                        continue
                #print view
                print(this.player.get_board().ships())
                print(ship_string)
                print(" All ships have been placed.")
            elif opt == "reset":
                this.player.get_board().clear_board()
                initialized = False
                #rebuilds menu
                ship_string = " 1: "+ship_dict[4]+"\n 2: "+ship_dict[3]+"\n 3: "+ship_dict[2]+"\n 4: "+ship_dict[1]+"\n 5: "+ship_dict[0]
                #prints view
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
        #--initialization of opponent and turn order
        selecting = True
        opponent_menu = [
            ("1", ": Easy", StupidAI),
            ("X", ": Normal [Under Development]", BasicAI),
            ("X", ": Hard   [Under Development]", AdvancedAI),
            ("X", ": Web    [Under Development]", WebPlayer)]
        opp_sel = StupidAI
        #----opponent selection
        while selecting:
            print(" Choose an opponent:")
            for o in opponent_menu:
                print(" "+o[0]+o[1])
            s = this.get_input()
            for o in opponent_menu:
                if s == o[0]:
                    opp_sel = o[2]
                    selecting = False
                    break
            if selecting:
                print(" Invalid opponent selection.")    
        order = 0#randint(0,1)
        opp = opp_sel()
        turn = order
        t = " "
        print(opp.name)
        #--loop
        playing = True #loop flag variable
        results = ["",""]
        while playing:
            #Opponent's turn
            if turn % 2 == 1:
                t = opp.turn(this.player)
                results[1-order] = " "+opp.name+"-> "+str(t[1])+": "+str(t[0])
            #checks if game is over
            if t[0] == "Gameover.":
                playing = False
                turn += 1
                continue
            print(this.player.get_board())
            if results[0] != "":
                print(results[0])
            if results[1] != "":
                print(results[1])
            player_turn = True
            while player_turn:
                sel = this.get_input("",split=True)
                print("")
                opt = sel[0]
                if opt == "help":
                    print("Options:")
                    print(" help  - displays this message")
                    print(" guess - makes a guess")
                    print("    usage:")
                    print("    guess [a-j][1-10]")
                    print("    example:")
                    print("    guess g4")
                    print(" board - prints the entire board")
                    print(" radar - prints just the radar portion of your board")
                    print(" clear - unclogs the screen")
                    print(" quit  - exits the program")
                    print("")
                elif opt == "guess":
                    #initial error checking
                    if len(sel) < 2:
                        print(" too few options specified")
                        continue
                    try:
                        c = this.str2coord(sel[1]) #coordinate
                        i = this.player.get_board().conv2int(c)
                    except ValueError:
                        print(" Invalid coordinates")
                        continue
                    t = opp.get_board().guess(i)
                    results[order] = " You-> "+str(t[1])+": "+str(t[0])
                    if t[0] != "Already guessed.":
                        turn += 1
                        n = "~"
                        if "Hit" in t[0]:
                            n = "!"
                        this.player.get_board().insert(n, this.player.get_board().conv2int(c), "radar")
                        player_turn = False
                elif opt == "board":
                    print(this.player.get_board())
                elif opt == "radar":
                    print(this.player.get_board().radar())
                elif opt == "clear":
                    clear_screen()
                elif opt == "quit":
                    playing = False
                    player_turn = False
                else:
                    print(" Unrecognized command sequence:")
                    print(" '"+" ".join(sel)+"'")
                    print(" Use command 'help' for help")
    
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
    