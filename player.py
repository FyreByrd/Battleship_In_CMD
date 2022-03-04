#player.py: contains class definitions for various types of players
#author: Aidan Jones
#AI algorithms are based off of: https://www.datagenetics.com/blog/december32011/

#<<<<<Import Statements>>>>>
from board import Board
from random import randrange as rand

#<<<<<Class Definitions>>>>>
#--base class for player
class Player():
    #--constructor
    def __init__(this,name:str):
        this.name = name
        this.score = 0
        this.board = Board()
    #--str conversion method
    def __str__(this):
        return this.name
    #--method to take a turn
    def turn(this, opponent):
        return "<Player.turn()> Not Implemented for use."
    #--method to get board. simply returns board
    #----will be overridden in WebPlayer class
    def get_board(this):
        return this.board
#--class for basic human player
class HumanPlayer(Player):
    #--constructor
    def __init__(this, name:str):
        super().__init__(name)
    #--returns result of calling board.get on opponent's board
    def turn(this, opponent:Player, c:tuple):
        i = this.board.conv2int(c)
        s = opponent.get_board().guess(i)
        if "Miss" in s:
            this.board.insert("O",c,"radar")
        elif "Hit" in s:
            this.board.insert("X",c,"radar")
        return s

#VVV#NOT IMPLEMENTED#VVV#
#--interface to play against an opponent through the internet
class WebPlayer(HumanPlayer):
    pass
#^^^#NOT IMPLEMENTED#^^^#

#--base class for an AI player
class AIPlayer(Player):
    def __init__(this, name:str="AI"):
        super().__init__(name)
        this.board.randomize()
#--AI that uses a PRNG to exhaust the board
class StupidAI(AIPlayer):
    def __init__(this, name:str="AI (Easy)"):
        super().__init__(name)
        this.guesses = []
    def turn(this, opp:Player):
        success = False
        if len(this.guesses) >= 100 or this.score >= 5:
            return ("Gameover.","")
        while not success:
            x = rand(0, 100)
            if x in this.guesses:
                continue
            else:
                t = opp.get_board().guess(x)
                this.guesses.append(x)
                if "Sunk" in t[0]:
                    this.score += 1
                return t
#--AI that uses a basic 2-stage Hunt/Target algorithm
class BasicAI(AIPlayer):
    #--constructor
    def __init__(this, name:str="AI (Normal)"):
        super().__init__(name)
        this.parity = []
        this.all = []
        #builds list of valid guesses
        for i in range(100):
            this.all.append(i)
        #builds list of parity guesses
        flip = 0
        for i in range(1, 100, 2):
            this.parity.append(i-flip)
            if i % 10 == 9:
                flip = 1 if flip == 0 else 0
        this.to_try = [] #coordinates to try
        this.mode = "Hunt"
    #--returns a random coordinate from parity or all
    def get_random_coord(this):
        if len(this.parity) > 0:
            r = rand(0,len(this.parity))
            i = this.parity[r]
            this.parity.remove(i)
            this.all.remove(i)
            return i
        elif len(this.all) > 0:
            r = rand(0,len(this.all))
            i = this.all[r]
            this.all.remove(i)
            return i
        else:
            print("Out of coordinates to guess")
            raise IndexError
    #--2-stage HUNT/TARGET algorithm with parity
    def turn(this, opp:Player):
        if this.score >= 5:
            return ("Gameover.", "")
        t = (" "," ")
        if len(this.to_try) > 0:
            this.mode = "TARGET"
        #TARGET mode
        if this.mode == "TARGET" and len(this.to_try) > 0:
            i = this.to_try.pop()
            this.all.remove(i)
            try:
                this.parity.remove(i)
            except ValueError:
                pass
            t = opp.get_board().guess(i)
        #HUNT mode
        else:
            i = this.get_random_coord()
            t = opp.get_board().guess(i)
        if "Hit" in t[0]:
            this.mode = "TARGET"
            neighbors = this.board.neighbors(i)
            for n in neighbors:
                if (n not in this.to_try) and (n in this.all) and (n != -1):
                    this.to_try.append(n)
            if "Sunk" in t[0]:
                this.score += 1
        return t

#VVV#NOT IMPLEMENTED#VVV#
#--AI that uses a Probability Density Function to aid a 2-stage Hunt/Target algorithm
class AdvancedAI(AIPlayer):
    pass
#^^^#NOT IMPLEMENTED#^^^#