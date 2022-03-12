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
        n = "~"
        if "Miss" in s[0]:
            this.board.insert("O",i,"radar")
        elif "Hit" in s[0]:
            this.board.insert("X",i,"radar")
            n = "!"
            if "Sunk" in s[0]:
                this.score += 1
        if "Already guessed" not in s[0]:
            this.board.insert(n, i, "radar")
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
                if (n not in this.to_try) and (n in this.all) and (n >= 0):
                    this.to_try.append(n)
            if "Sunk" in t[0]:
                this.score += 1
        return t
#--AI that uses a Probability Density Function to aid a 2-stage Hunt/Target algorithm
class AdvancedAI(AIPlayer):
    #--constructor
    def __init__(this, name:str="AI (Hard)"):
        super().__init__(name)
        this.mode = "HUNT"
        this.parity = ([1, 0] * 5 + [0, 1] * 5) * 5
        this.misses = []
        this.unlikely = []
        this.hits = []
        this.sinks = []
        this.guesses = []
        this.probability_cloud = [0] * 100
        this.max_index = 0
    #--returns a boolean value based on impassability at coordinate i
    def is_impassable(this, i:int):
        b = (i in this.misses) or (i in this.unlikely) or (i in this.sinks)
        if this.mode == "HUNT":
            b |= (i in this.hits)
        return b
    #--analyzes current hits to determine necessary mode and unlikely
    def analyze_hits(this):
        this.unlikely.clear()
        #build list of hits with coordinates
        hits_and_neighbors = []
        for h in this.hits:
            hits_and_neighbors.append((h, this.board.neighbors(h)))
        #analyze list
        hit = lambda i: i in this.hits or i == -1 #hit or edge
        c = lambda b: 1 if b else 0
        for h in hits_and_neighbors:
            n = h[1]
            h_neighbors = []
            colinear = (hit(n[0]) and hit(n[2])) or (hit(n[1]) and hit(n[3]))
            for i in range(4):
                if hit(n[i]):
                    h_neighbors.append(n[i]) 
                    if hit(this.board.neighbors(n[i])[i]):
                        colinear = True
            if len(h_neighbors) > 3 or colinear:
                this.unlikely.append(h[0])
    #--builds a probability cloud for all the ships and puts it in this.probability cloud
    def build_probability_cloud(this):
        p_output = []
        clouds_to_build = [(5, 0), (5, 1), (4, 0), (4, 1), (3, 0), (3, 1), (3, 0), (3, 1), (2, 0), (2, 1)]
        #builds a cloud for each ship length and orientation
        for c in clouds_to_build:
            this.build_help(c[0], c[1], p_output)
        #sums all the values across the subclouds
        for i in range(100):
            sum = 0
            if this.is_impassable(i):
                this.probability_cloud[i] = -10
                continue
            elif i in this.guesses:
                this.probability_cloud[i] = -1
                continue
            elif this.mode == "HUNT":
                for p in p_output:
                    sum += p[i] + this.parity[i]
            else:
                for p in p_output:
                    sum += p[i]
                sum += this.parity[i]
            if sum > this.probability_cloud[this.max_index]:
                this.max_index = i
            this.probability_cloud[i] = sum
    #--builds a complete cloud for one ship of length l, orientation dir
    def build_help(this, l:int, dir:int, out:list):
        cloud = [0] * 100
        for i in range(100):
            available = True
            inds = []
            hits_count = 0
            for j in range(i, i + l * 10 ** dir, 10 ** dir):
                inds.append(j)
                if j >= 100:
                    available = False
                    break
                if this.mode == "TARGET":
                    if j in this.hits and i not in this.unlikely:
                        hits_count += 1
                if this.is_impassable(j):
                    available = False
                elif j % 10 == 9 and j != i + (l - 1) * 10 ** dir:
                    if j < 99:
                        k = j + 10**dir
                        if k % 10 == 0:
                            available = False
            if available:
                for j in inds:
                    cloud[j] += 1 if this.mode == "HUNT" else hits_count * 5
        out.append(cloud)
    #--2-stage HUNT/TARGET algorithm with parity
    #----uses a probability cloud to make better guesses
    #----uses an endgame heuristic to mitigate chokes
    def turn(this, opp:Player):
        if this.score >= 5:
            return ("Gameover.", "")
        this.build_probability_cloud()
        i = this.max_index
        this.guesses.append(i)
        t = opp.get_board().guess(i)
        this.probability_cloud[i] = -1
        if "Miss" in t[0]:
            this.misses.append(i)
        if "Hit" in t[0]:
            this.mode = "TARGET"
            this.hits.append(i)
            if "Sunk" in t[0]:
                this.mode = "HUNT"
                this.sinks.append(i)
                this.score += 1
                this.analyze_hits()
        #anti-choke heuristic
        if len(this.guesses) > 50 + len(this.hits)//2:
            this.unlikely.clear()
            this.mode = "TARGET"
        return t
