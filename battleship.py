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
        inp = input(" "+msg+"> ")
        inp = str(inp)
        inp = inp.strip()
        if not case_sensitive:
            inp = inp.lower()
        return inp.split(div) if split else inp  
    #--constructor
    def __init__(this):
        pname = this.get_input("Type the name you would like to use ",case_sensitive=True)
        this.player = HumanPlayer(pname)
        this.opp = HumanPlayer("ai")
        print(" Welcome, "+str(this.player))
        print(" Type 'help' to list available commands")
    
    #--main loop function
    def main_loop(this):
        playing = True
        print(" Enter your desired command...")
        while playing:
            sel = this.get_input("",split=True)
            opt = sel[0]
            if opt == "help":
                print(" Options:")
                print(" help   - displays this message")
                print(" whoami - displays your username")
                #print(" new    - creates new game")
                #print("       options:")
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
            elif opt == "clear":
                clear_screen()
            elif opt == "quit":
                playing = False
            else:
                print(" Unrecognize command sequence:")
                print(" '"+" ".join(sel)+"'")
                print(" Use command 'help' for help")

#--Main method
if __name__=="__main__":
    clear_screen()
    print(welcome_string)
    game = BattleShipMain()
    game.main_loop()
    