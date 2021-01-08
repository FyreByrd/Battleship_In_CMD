import board
from random import choice, randint

class BasicAI:
    def __init__(self, radar, opp):
        self.radar = radar
        self.opp = opp
        self.grid_1 = []
        self.all = []
        for i in range(100):
            c = self.radar.coords_from_rawcoord(i)
            self.all.append(c)
        flip = 0
        for i in range(1,100,2):
            c = self.radar.coords_from_rawcoord(i-flip)
            self.grid_1.append(c)
            if i % 10 == 9:
                flip = 1 if flip == 0 else 0
        self.hits = []
        self.nchecked = []
        self.totry = []
        self.mode = "Hunt"
    def guess(self, guesses = 1,blah=False):
        output = ""
        int_to_char = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J"}
        for g in range(guesses):
            if self.mode == "Hunt" and len(self.totry) > 0:
                self.mode = "Target"
            if self.mode == "Target":
                # check unchecked hits for valid neighbors
                for h in self.hits:
                    if h not in self.nchecked:
                        to_try = self.opp.neighbors_of_coord(h)
                        for c in to_try:
                            if c in self.all:
                                self.totry.insert(0,c)
                        self.nchecked.append(h)
                if len(self.totry) > 0:
                    coords = self.totry.pop()
                else:
                    self.mode = "Hunt"
            if self.mode == "Hunt":
                if len(self.grid_1) > 0:
                    coords = self.grid_1[randint(0,len(self.grid_1)-1)]
                else:
                    coords = self.all[randint(0,len(self.all)-1)]
            val = self.opp.guess(coords, self.radar)
            if coords in self.grid_1:
                self.grid_1.remove(coords)
            if coords in self.all:
                self.all.remove(coords)
            if "Hit" in val:
                self.hits.append(coords)
                self.mode = "Target"
            output += " AI guessed "+int_to_char[coords[0]]+" "+str(coords[1]//2+1)+"\n"+val+"\n"
        return output
class AdvancedAI:
    def __init__(self, radar, opp):
        self.opp = opp
        self.pcloud = []
        k = 0
        for i in range(100):
            if k == 0 and i % 10 == 9:
                k = -1
            elif k == -1 and i % 10 == 9:
                k = 0
            j = i + k
            self.pcloud.append(0)
        self.weights = [2,3,3,4,5]
        self.hits = []
        self.sinks = []
        self.radar = radar
        self.mode = "Hunt"
    def remove_coord(self, coord):
        if type(coord) == tuple:
            coord = self.opp.rawcoord_from_coords(coord)
        self.pcloud[coord] = -2
        if coord in self.hits:
            self.pcloud[coord] = -1
    def try_fit(self, start, dir, length, limit=0):
        if type(start) == tuple:
            start = self.opp.rawcoord_from_coords(start)
        output = [""]
        if dir % 2 == 1:
            n = start % 10
            for i in range(start, start+length):
                if i % 10 < n:
                    output.clear()
                    output.append("edge")
                    return output
                if self.pcloud[i] < limit:
                    output.clear()
                    output.append("blocked")
                    output.append(i)
                    return output
                output.append(i)
        elif dir % 2 == 0:
            for i in range(start, start+(10*length),10):
                if i > 99:
                    output.clear()
                    output.append("edge")
                    return output 
                if self.pcloud[i] < limit:
                    output.clear()
                    output.append("blocked")
                    output.append(i)
                    return output
                output.append(i)
        return output
    def update_clouds(self, targeting=False):
        for i in range(100):
            if not self.pcloud[i] < 0:
                self.pcloud[i] = 0
            if i in self.hits:
                self.pcloud[i] = -1
        for i in range(100):
            lim = -1 if targeting else 0
            if self.pcloud[i] < lim:
                continue
            for j in self.weights:
                bonus1 = 0
                bonus2 = 0
                result = self.try_fit(i, 0, j, lim)
                result2 = self.try_fit(i, 1, j, lim)
                valid1 = not targeting
                valid2 = not targeting
                if targeting:
                    for k in range(1,len(result)):
                        if result[k] in self.hits:
                            valid1 = True
                            bonus1 += 5
                    for k in range(1,len(result2)):
                        if result2[k] in self.hits:
                            valid2 = True
                            bonus2 += 5
                if result[0] == "":
                    for k in range(1,len(result)):
                        if not valid1:
                            continue
                        if self.pcloud[result[k]] in self.hits:
                            continue
                        self.pcloud[result[k]] += 1 + bonus1                
                if result2[0] == "":
                    for k in range(1,len(result2)):
                        if not valid2:
                            continue
                        if self.pcloud[result2[k]] in self.hits:
                            continue
                        self.pcloud[result2[k]] += 1 + bonus2
                if (not result[0] == "") and (not result[0] == ""):
                    break
            if i in self.hits:
                self.pcloud[i] = -1
    def check_prob_cloud(self,testing=False):
        cloud = []
        i = 0
        max_index = 0
        max_val = -1
        for i in range(100):
            cloud.append(0)
            cloud[i] += self.pcloud[i]
            if cloud[i] > max_val:
                max_index = i
                max_val = cloud[i]
        if not testing:
            print(" Probability Cloud:")   
            self.print_cloud(cloud)
            print(" "+str(max_index)+": "+str(max_val))
        return self.opp.coords_from_rawcoord(max_index)
    def print_cloud(self, cloud):
        output = "    1   2   3   4   5   6   7   8   9  10\n"
        int_to_char = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J"}
        for i in range(100):
            output += " "
            if i % 10 == 0:
                output += int_to_char[i/10] + " "
            if cloud[i] < 10 and cloud[i] >= 0:
                output += "0"+str(cloud[i])
            else:
                output += str(cloud[i])    
            output += " "    
            if i % 10 == 9:
                output += "\n\n"
        print(output)
    def guess(self, guesses = 1, testing = False):
        output = ""
        int_to_char = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J"}
        for g in range(guesses):
            self.update_clouds((True if self.mode == "Target" else False))
            coords = self.check_prob_cloud(testing)
            val = self.opp.guess(coords, self.radar)
            if "Hit" in val:
                self.hits.append(self.opp.rawcoord_from_coords(coords))
                self.mode = "Target"
            if "Sunk" in val:
                self.sinks.append(self.opp.rawcoord_from_coords(coords))
                self.mode = "Hunt"
            self.remove_coord(coords)
            if not testing:
                print(" Hits: "+str(self.hits)) 
                print(" Mode: "+self.mode)
            output += " AI guessed "+int_to_char[coords[0]]+" "+str(coords[1]//2+1)+"\n"+val+"\n"
        return output
