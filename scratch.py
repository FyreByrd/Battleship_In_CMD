from player import AIPlayer, Player

#--AI that uses a Probability Density Function to aid a 2-stage Hunt/Target algorithm. Augmented with bit manipulation.
class FastAdvancedAI(AIPlayer):
    #--constructor
    def __init__(this, name:str="AI (Fast?)"):
        super().__init__(name)
        this.hunting = True
        # lower corner is index 0
        this.parity = 0xaa955aa955aa955aa955aa955
        this.misses = 0
        this.unlikely = 0
        this.hits = 0
        this.sinks = 0
        this.guesses = 0
        this.probability_cloud = [0] * 100
        this.max_index = 0
        this.num_guesses = 0
        this.num_hits = 0 
        this.h_ships = [(0x1f, 5), (0xf,4), (0x7,3), (0x7,3), (0x3,2)]
        this.v_ships = [(0x10040100401, 5), (0x40100401,4), (0x100401,3), (0x100401,3), (0x401,2)]
    #--returns a boolean value based on impassability at coordinate i
    def is_impassable(this, i:int):
        b = (this.misses | this.unlikely | this.sinks)
        if this.hunting:
            b |= this.hits
        return (b & (0x1 << i)) != 0
    #--analyzes current hits to determine necessary mode and unlikely
    def analyze_hits(this):
        this.unlikely = 0
        #build list of hits with coordinates
        hits_and_neighbors = []
        for h in range(100):
            if (this.hits & (0x1 << h)) != 0:
                hits_and_neighbors.append((h, this.board.neighbors(h)))
        #analyze list
        hit = lambda i: i < 0 or (this.hits & (0x1 << i)) != 0 #hit or edge
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
                this.unlikely |= 0x1 << h[0]
    #--builds a probability cloud for all the ships and puts it in this.probability cloud
    def build_probability_cloud(this):
        for i in range(100):
            this.probability_cloud[i] = 0
        bmp = this.guesses
        if not this.hunting:
            bmp = this.misses | this.unlikely | this.sinks
        #builds a cloud for each ship length and orientation
        for s in range(len(this.h_ships)):
            m = this.h_ships[s][0]
            l = this.h_ships[s][1]
            for i in range(101 - l):
                if i % 10 > (10 - l):
                    m <<= 1
                    continue
                if m & bmp == 0:
                    if not this.hunting and m & this.hits == 0:
                        m <<= 1 
                        continue
                    for j in range(i, i + l):
                        this.probability_cloud[j] += 1
                m <<= 1
        for s in range(len(this.v_ships)):
            m = this.v_ships[s][0]
            l = this.v_ships[s][1]
            for i in range(110 - l*10):
                if m & bmp == 0:
                    if not this.hunting and m & this.hits == 0:
                        m <<= 1 
                        continue
                    for j in range(i, i + l * 10, 10):
                        this.probability_cloud[j] += 1
                m <<= 1        
        #finds max value in probability cloud
        this.max_index = 0
        for i in range(100):
            if this.is_impassable(i):
                this.probability_cloud[i] = -10
                continue
            elif (this.guesses >> i) & 0x1 != 0:
                this.probability_cloud[i] = -1
                continue
            else:
                this.probability_cloud[i] += ((this.parity >> i) & 0x1)
            if this.probability_cloud[i] > this.probability_cloud[this.max_index]:
                this.max_index = i
    def cloud2str(this):
        s = "    "
        d = {
            -10:"X",
            -1: "x",
            0: " ",
            10:"_",
            20:"-",
            30:"n",
            40:"m",
            50:"=",
            60:"A",
            70:"M",
            80:"&",
            90:"^"
        }
        for i in range(100):
            s += str(this.probability_cloud[i])+" "#d[10 * (this.probability_cloud[i]//10)]+" "
            if i % 10 == 9:
                s += "\n    "
        return s
    #--2-stage HUNT/TARGET algorithm with parity
    #----uses a probability cloud to make better guesses
    #----uses an endgame heuristic to mitigate chokes
    def turn(this, opp:Player):
        if this.score >= 5:
            return ("Gameover.", "")
        this.build_probability_cloud()
        #print(this.cloud2str())
        i = this.max_index
        this.guesses |= 0x1 << i
        this.num_guesses += 1
        t = opp.get_board().guess(i)
        this.probability_cloud[i] = -1
        if "Miss" in t[0]:
            this.misses |= 0x1 << i
        if "Hit" in t[0]:
            this.hunting = False
            this.hits |= 0x1 << i
            this.num_hits += 1
            if "Sunk" in t[0]:
                this.hunting = True
                this.sinks |= 0x1 << i
                this.score += 1
                #print("sunk")
                this.analyze_hits()
        #anti-choke heuristic
        if this.num_guesses > 50 + this.num_hits//2:
            this.unlikely = 0
            this.hunting = False
        return t
    def clear_state(this):
        super().clear_state()
        this.hunting = True
        this.misses = 0
        this.unlikely = 0
        this.hits = 0
        this.sinks = 0
        this.guesses = 0
        this.max_index = 0
        this.num_guesses = 0
        this.num_hits = 0
