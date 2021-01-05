class Board:
    def __init__(self):
        self.board = []
        self.rows = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8,"j":9}
        self.raw = []
        i = 0
        for i in range(10):
            row = " . . . . . . . . . "
            self.board.append(row)
        for i in range(100):
            self.raw.append("0")
    def display_board(self):
        letters = ('A','B','C','D','E','F','G','H','I','J')
        output = ["    1.2.3.4.5.6.7.8.9.10"]
        for i in range(len(self.board)):
            output.append(" "+letters[i]+"| "+self.board[i]+" |")
        return "\n".join(output)
    def coords_from_input(self, row, col):
        col = int(col)
        if col == 0:
            col = 10
        return (self.rows[row], 2*(col-1))
    def rawcoord_from_input(self, row, col):
        col  = int(col)
        if col == 0:
            col = 10
        row = self.rows[row]
        return (10*row)+(col-1)
    def coords_from_rawcoord(self, rcoord):
        rcoord = int(rcoord)
        return ((rcoord - (rcoord % 10)) // 10, (rcoord % 10) * 2)
    def rawcoord_from_coords(self, coords):
        return (coords[0] * 10) + (coords[1] // 2)
    def north(self, coord):
        return "" if coord[0] <= 0 else (coord[0] - 1, coord[1])
    def east(self, coord):
        return "" if coord[1] >= 9 else (coord[0], coord[1] + 2)
    def south(self, coord):
        return "" if coord[0] >= 9 else (coord[0] + 1, coord[1])
    def west(self, coord):
        return "" if coord[1] <= 0 else (coord[0], coord[1] - 2)
    def neighbors_of_coord(self, coords):
        n = self.north(coords)
        e = self.east(coords)
        s = self.south(coords)
        w = self.west(coords)
        neighbors = []
        if not n == "":
            neighbors.append(n)
        if not e == "":
            neighbors.append(e)
        if not s == "":
            neighbors.append(s)
        if not w == "":
            neighbors.append(w)
        return neighbors
    def val_at_coords(self, coords):
        try:
            s = self.board[coords[0]]
            return s[coords[1]]
        except IndexError:
            print("IndexError")
            print(self.display_board())
            print(str(coords)+" "+str(s)+" "+str(len(s)))
            raise
    def set_at_coords(self, coords, val):
        row = self.board[coords[0]]
        x = coords[1]
        row = row[:x]+str(val)+row[x+1:]
        self.board[coords[0]] = row
    def guess(self, coords, radar):
        a = coords[0]
        b = coords[1]
        test = self.val_at_coords(coords)
        if test == "X" or test == "-" or radar.val_at_coords(coords) == "O" or radar.val_at_coords(coords) == "X":
            return " Already guessed. Try again"
        elif test == " ":
            radar.set_at_coords(coords, "O")
            self.set_at_coords(coords, "-")
            return " Miss!"
        else:
            self.set_at_coords(coords, "X")
            rc = self.rawcoord_from_coords(coords)
            test = self.raw[rc]
            self.raw[rc] = "X"
            radar.set_at_coords(coords, "X")
            if test not in self.raw:
                return " Hit and Sunk!"
            return " Hit!"
    def try_insert_ship(self, coords, length, dir):
        if self.val_at_coords(coords) == " ":
            if dir == 0:
                ncoords = coords
                for i in range(length):
                    ncoords = self.north(ncoords)
                    if ncoords == "" or not (self.val_at_coords(ncoords) == " "):
                        return "ship won't fit. try new position or orientation"
            elif dir == 1:
                ncoords = coords
                for i in range(length):
                    ncoords = self.east(ncoords)
                    if ncoords == "" or not (self.val_at_coords(ncoords) == " "):
                        return "ship won't fit. try new position or orientation"
            else:
                return "invalid direction"
            return "ship placed successfully"
        else:
            return "coordinates occupied"

    def insert_ship(self, coords, ship, ship_id, dir):
        y = coords[0]
        x = coords[1]
        test = self.try_insert_ship(coords, len(ship), dir)
        if "success" not in test:
            return test
        if dir == 1:
            s = self.board[y]
            insert = s[:x]
            a = x
            for c in ship:
                insert += c+"."
                self.raw[self.rawcoord_from_coords((y,a))] = str(ship_id)
                a += 2
            b = 2 * len(ship)
            insert += s[x+b:]
            self.board[y] = insert
        else:
            a = y
            for c in ship:
                self.board[a] = self.board[a][:x] + c + self.board[a][x+1:]
                self.raw[self.rawcoord_from_coords((a,x))] = str(ship_id)
                a -= 1
        return test
