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
#--interface to play against an opponent through the internet
class WebPlayer(HumanPlayer):
    pass
#--base class for an AI player
class AIPlayer(Player):
    def __init__(this, name:str="AI"):
        super().__init__(name)
        this.board.randomize()
#--AI that uses a PRNG to exhaust the board
class StupidAI(AIPlayer):
    def __init__(this, name:str="AI (Easy)"):
        super().__init__(name)
        this.sunkcount = 0
        this.guesses = []
    def turn(this, opp:Player):
        success = False
        if len(this.guesses) >= 100 or this.sunkcount >= 5:
            return "Gameover."
        while not success:
            x = rand(0, 100)
            if x in this.guesses:
                continue
            else:
                t = opp.get_board().guess(x)
                this.guesses.append(x)
                if "Sunk" in t[0]:
                    this.sunkcount += 1
                return t
#--AI that uses a basic 2-stage Hunt/Target algorithm
class BasicAI(AIPlayer):
    pass
#--AI that uses a Probability Density Function to aid a 2-stage Hunt/Target algorithm
class AdvancedAI(AIPlayer):
    pass
