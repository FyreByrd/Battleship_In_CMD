#board.py: contains classes Ship, and Board
#Author: Aidan Jones

#<<<<<Import Statements>>>>>
from random import randrange

#--container for text representations of the ships
class Ship:
    def __init__(this):
        horizontal = ["[###]","<ss>","co>","cf>","c>"]
        vertical = ["=HHH=","AHHV","^OU","^@U","^U"]
        this.ships = (horizontal, vertical)
        this.uniq = {"#":0,"=":0,"s":1,"V":1,"o":2,"O":2,"f":3,"@":3}

#--Represents a player's playing area
class Board:
    #<<<<<Constructor>>>>>
    def __init__(this):
        this.data = {"board":"0"*100, "radar":"0"*100, "raw":"0"*100}
        this.rows = "abcdefghij"
        this.shipdict = Ship()
        this.coord_array = [
            "A1","A2","A3","A4","A5","A6","A7","A8","A9","A10",
            "B1","B2","B3","B4","B5","B6","B7","B8","B9","B10",
            "C1","C2","C3","C4","C5","C6","C7","C8","C9","C10",
            "D1","D2","D3","D4","D5","D6","D7","D8","D9","D10",
            "E1","E2","E3","E4","E5","E6","E7","E8","E9","E10",
            "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10",
            "G1","G2","G3","G4","G5","G6","G7","G8","G9","G10",
            "H1","H2","H3","H4","H5","H6","H7","H8","H9","H10",
            "I1","I2","I3","I4","I5","I6","I7","I8","I9","I10",
            "J1","J2","J3","J4","J5","J6","J7","J8","J9","J10",]
        this.last_guessed = -1

    #<<<<<Output Functions>>>>>
    #--formats board as string for printing
    def __str__(this):
        out = " _________________________ \n"
        out +="|## 1 2 3 4 5 6 7 8 9 10##|\n"
        out +="|#########################|\n"
        for i in range(10):
            out += "|"+this.rows[i]+"#"
            for j in range(10):
                k = j + 10*i
                out += "."+str(this.dat2char(k, "radar"))
            out += ".#"+this.rows[i]+"|\n"
        out +="|#########################|\n"
        out +="|## 1 2 3 4 5 6 7 8 9 10##|\n"
        out +="'^^^^^^^^^^^^^^^^^^^^^^^^^'\n"
        out +="|VVVVVVVVVVVVVVVVVVVVVVVVV|\n"
        out +="|## 1 2 3 4 5 6 7 8 9 10##|\n"
        out +="|#########################|\n"
        g = -1#this.last_guessed
        for i in range(10):
            out += "|"+this.rows[i]+"#"
            for j in range(10):
                k = j + 10*i
                if (g != -1) and (k == g or (k - 1 == g and k%10 != 0 and (k-1)%10 != 9)):
                    out += "|"+str(this.dat2char(k, "board"))
                else:  
                    out += "."+str(this.dat2char(k, "board"))
            out += "|" if i*10+9 == g else "."
            out += "#"+this.rows[i]+"|\n"
        out +="|#########################|\n"
        out +="|## 1 2 3 4 5 6 7 8 9 10##|\n"
        out +="'^^^^^^^^^^^^^^^^^^^^^^^^^'"
        return out
    #--inputs guess(g) into the board, then returns as a tuple:
    #----"Already guessed." if g has been guessed before
    #----"Miss." if the guess is a miss
    #----"Hit and Sunk." if it is a sinking hit
    #----or "Hit." if it is a non-sinking hit
    #----with the second element as the string representation of the coordinate
    #--will raise ValueError if the guess is out of bounds 
    def guess(this, g):
        g = this.conv2int(g)
        if g not in range(100):
            print("Error: guess out of bounds of board")
            raise ValueError
        else:
            t = this.data["raw"][g]
        if t == "G":
            r = "Already guessed."
        elif t == "0":
            this.insert("G", g, "raw")
            this.insert("~", g, "board")
            r = "Miss."
        else:
            x = this.insert("G", g, "raw")
            this.insert("!", g, "board")
            if x not in this.data["raw"]:
                r = "Hit and Sunk."
            else:
                r = "Hit."
        this.last_guessed = g
        return (r, this.coord_array[g])
    #--returns just the radar portion of the board as a string
    def radar(this):
        s = this.__str__()
        return s[:447]
    #--returns just the ship portion of the board as a string
    def ships(this):
        s = this.__str__()
        return s[:27]+s[475:]
    
    #<<<<<Helper Functions>>>>>
    #--returns a more helpful representation of the data in the board selected by arr
    def dat2char(this, i:int, arr:str):
        arr = this.data[arr]
        if arr[i] == "0":
            return " "
        elif arr[i] == "~":
            return "~"
        elif arr[i] == "!":
            return "&"
        else:
            return arr[i]
    #--converts i to an integral index for the arrays
    #----expected types:
    #------ int: [0,99]
    #------ tuple : (str : [a,j] or int: [0,9] , int: [0,9], ...)
    #------ str : "[a-j][0-9]*"
    #----will not throw error if int is out of specified range
    #----will throw error if:
    #------input is not one of the above types
    #------the second index cannot be converted to int
    #------the first index is not in range
    def conv2int(this, i):
        if type(i) == int:
            return i
        elif type(i) == tuple:
            if type(i[0]) == str:
                return 10 * this.rows.index(i[0]) + int(i[1])
            else:
                return 10 * int(i[0]) + int(i[1])
        elif type(i) == str:
            return 10 * this.rows.index(i[0]) + int(i[1])
        else:
            raise TypeError
    #--inserts c in board arr at index ind and returns the old value at ind
    def insert(this, c, ind:int, arr:str):
        if ind not in range(100):
            raise ValueError
        else:
            t = this.data[arr][ind]
            this.data[arr] = this.data[arr][:ind]+str(c)+this.data[arr][ind+1:]
            return t
    #--clears the board
    def clear_board(this):
        this.data = {"board":"0"*100, "radar":"0"*100, "raw":"0"*100}
    
    #<<<<<Coordinate Neighbor Functions
    #--returns coordinate directly above
    def u(this, c:int):
        return c - 10 if c - 10 >= 0 else -1
    #--returns coordinate directly below
    def d(this, c:int):
        return c + 10 if c + 10 < 100 else -1
    #--returns coordinate directly to the left
    def l(this, c:int):
        return c - 1 if c % 10 != 0 else -1
    #--returns coordinate directly to the right
    def r(this, c:int):
        return c + 1 if c % 10 != 9 else -1
    #--returns coordinate's four neighbors as a tuple in clockwise order from the top
    def neighbors(this, c:int):
        return (this.u(c), this.r(c), this.d(c), this.l(c))

    #<<<<<Ship Placement Functions>>>>>
    #--generates a random board
    def randomize(this):
        ships = [(5,"5"),(4,"4"),(3,"3"),(3,"2"),(2,"1")]
        for s in range(len(ships)):
            success = False
            while not success:
                dir = randrange(0,2)
                ind = randrange(0, 100)
                success = this.insert_ship(ind,dir,s,ships[s][1])         
    #--inserts a ship at index ind with orientation dir and raw representation ch
    #----dir is 0 for horizontal and 1 for vertical
    #----returns False if ship cannot be placed as specified
    def insert_ship(this, ind:int, dir:int, ship:int, ch:str):
        s = this.shipdict.ships[dir][ship]
        l = len(s)
        available = True
        for i in range(ind, ind + l * 10 ** dir, 10 ** dir):
            if i >= 100:
                available = False
            elif this.data["raw"][i] != "0":
                available = False
            elif i % 10 == 9  and i != ind + (l - 1) * 10 ** dir:
                if i < 99:
                    j = i + 10**dir
                    if j % 10 == 0:
                        available = False 
        if available:
            n = range(l)
            inds = range(ind, ind + l * 10 ** dir, 10 ** dir)
            for i in n:
                this.insert(s[i],inds[i],"board")
                this.insert(ch,inds[i],"raw")
        return available
    #--removes a ship matching ch in the raw data array
    def remove_ship(this, ch:str):
        s = ""
        while ch in this.data["raw"]:
            i = this.data["raw"].index(ch)
            this.insert("0", i, "raw")
            s += this.insert("0", i, "board")
        r = this.find_ship_by_uniq(s)
        if r[0]:
            return "Removed: "+r[1]
        else:
            return "No ship was removed."
    #--searches for horizontal representation of ship by indicators in s
    def find_ship_by_uniq(this, s:str):
        match = False
        for c in s:
            try:
                if not match:
                    s = this.shipdict.ships[0][this.shipdict.uniq[c]]
                    match = True
            except (ValueError, KeyError):
                match = False
                continue
        if not match:
            if len(s) == 2:
                s = this.shipdict.ships[0][4]
                match = True
        return (match, s)
