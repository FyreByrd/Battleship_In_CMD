import os
from random import randint, choice
import battleai as ai
import misc
from board import Board
from ships import Ships
from analysis import analyze
from time import time

welcome = """
 _________________________________________________________
     ____                                __                    
     /   )                  /          /    ) /     ,        
    /__ /    __  _/_  _/_  /   __      \     /__       __ 
   /    )  /   ) /    /   /  /___)      \   /   ) /  /   )
  /____/  (___( (    (   /  (___    (____/ /   / /  /___/ 
                                                   /      
                                                  / 
 _____command_line________________________________________      
"""
class BattleShipMain:
    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')
    def rand_c(self):
        return 2 * randint(0,99) + randint(0,1)
    def get_input(self, msg, case=False, split=False, div=" "):
        inp = input(" "+str(msg)+": ")
        inp = str(inp)
        if not case:
            inp = inp.lower()
        if split:
            return inp.split(div)
        else:
            return inp.strip()
    def __init__(self):
        self.clear()
        print(welcome)
        self.player = self.get_input("type the name you would like to use",case=True)
        print(" Welcome, "+self.player)
        print(" type 'help' to list available commands")
        self.state = misc.StateManager("Main Menu")
        ships = Ships()
        self.ship_types = {"tug":ships.tugh, "tug-alt":ships.tugv,"sub":ships.subh, "sub-alt":ships.subv,"bat":ships.bath, 
            "bat-alt":ships.batv,"des":ships.desh, "des-alt":ships.desv,"air":ships.airh, "air-alt":ships.airv}
        self.ship_ids = {"tug":"t", "tug-alt":"t","sub":"s", "sub-alt":"s","bat":"b", 
            "bat-alt":"b","des":"d", "des-alt":"d","air":"a", "air-alt":"a"}
        self.ship_opts = ["air","des","bat","sub","tug"]
    def random_board(self, board):
        c = self.rand_c()
        for s in self.ship_opts:
            while True:
                if c % 2 == 1:
                    d = 1
                    coords = (c - 1)//2
                    ship = self.ship_types[s]
                else:
                    d = 0
                    coords = c//2
                    ship = self.ship_types[s+"-alt"]
                coords = board.coords_from_rawcoord(coords)
                if "success" not in board.insert_ship(coords,ship,self.ship_ids[s], d):
                    c = self.rand_c()
                else:
                    break
    def test_winner(self, p1, p2, scman):
        return True if (scman.get_score(p1) > 4 or scman.get_score(p2) > 4) else False
    def get_winner(self, p1, p2, scman):
        if self.test_winner(p1,p2,scman):
            return p1 if scman.get_score(p1) > scman.get_score(p2) else p2
        else:
            return None
    def test_ai(self, com):
        num = int(self.get_input("enter the number of tests you would like to run"))
        t_0 = time()
        advanced = True if "a" in com else False
        sink_1 = []
        sink_2 = []
        sink_3 = []
        sink_4 = []
        turns_taken = []
        continuing = True
        intervals = [1,10,100,1000,10000,100000,1000000]
        interval_vals = {1:1,10:10,100:10,1000:100,10000:100,100000:1000,1000000:5000}
        update_interval = 1
        last_printed = 0
        for i in range(len(intervals)):
            if num >= intervals[i]:
                update_interval = interval_vals[intervals[i]]
        for i in range(num):
            if not continuing:
                break
            sinks = 0
            turn = 0
            board = Board()
            radar = Board()
            vals = []
            #print(" Generating Board")
            self.random_board(board)
            tester = ai.AdvancedAI(radar,board) if advanced else ai.BasicAI(radar,board)
            #print(" Commencing Test "+str(i))
            while sinks < 5:
                try:
                    turn += 1
                    val = tester.guess(1,True)
                    vals.append(val)
                    if "Sunk" in val:
                        sinks += 1
                        if sinks == 1:
                            #print(" 1st: "+str(turn))
                            sink_1.append(turn)
                        elif sinks == 2:
                            #print(" 2nd: "+str(turn))
                            sink_2.append(turn)
                        elif sinks == 3:
                            #print(" 3rd: "+str(turn))
                            sink_3.append(turn)
                        elif sinks == 4:
                            #print(" 4th: "+str(turn))
                            sink_4.append(turn)
                except KeyboardInterrupt:
                    continuing = False
                    print(" Guesses Until Interrupt:"+str(turn))
                    for v in vals:
                        print(val)
                    if advanced:
                        tester.print_cloud(tester.pcloud)
                    print(tester.opp.display_board())
                    break
                
            #print(" Guesses: "+str(turn))
            #print(" Test "+str(i)+" Complete")
            if i+1 > last_printed + update_interval:
                print(i)
                last_printed = i
            turns_taken.append(turn)
        print(" Tests: "+str(num))
        print(analyze(sink_1, "Guesses to first sunk ship"))
        print(analyze(sink_2, "Guesses to second sunk ship"))
        print(analyze(sink_3, "Guesses to third sunk ship"))
        print(analyze(sink_4, "Guesses to fourth sunk ship"))
        print(analyze(turns_taken, "Total Guesses"))
        print(" Time taken: "+str(time() - t_0))
        self.state.set("Main Menu")
        print("\n\n Main Menu")
    def matchup_ai(self):
        num = int(self.get_input("enter the number of tests you would like to run"))
        t_0 = time()
        results = []
        lengths = []
        aname = "advanced"
        bname = "basic"
        for i in range(num):
            aradar = Board()
            aboard = Board()
            bradar = Board()
            bboard = Board()
            aia = ai.AdvancedAI(aradar,bboard)
            aib = ai.BasicAI(bradar,aboard)
            self.random_board(aboard)
            self.random_board(bboard)
            scman = misc.ScoreManager(aname,bname)
            winner = 0
            turn = 0
            starting = randint(0,1)
            while not self.test_winner(aname,bname,scman):
                turn += 1
                t = turn % 2
                if t == starting:
                    val = aia.guess(1,True)
                    if "Sunk" in val:
                        scman.inc_score(aname)
                else:
                    val = aib.guess()
                    if "Sunk" in val:
                        scman.inc_score(bname)
            else:
                results.append(1 if self.get_winner(aname,bname,scman) == aname else 0)
                lengths.append(turn)
        print(analyze(results, "Wins"))
        print(analyze(lengths,"Average Game Length"))
        print(" Time taken: "+str(time() - t_0))
        self.state.set("Main Menu")
        print("\n\n Main Menu")

    def loop(self):
        while True:
            if self.state.get() == "Main Menu":
                com = self.get_input("")
                if "help" in com:
                    print("    Available Commands:")
                    print(" help   - lists available commands")
                    print(" exit   - exits the program")
                    print(" whoami - displays your username")
                    print(" new    - creates new game")
                    print("       options:")
                    print("     -c - choose your setup [TBI]")
                    print("     -s - salvo mode")
                    print("     -a - advanced AI")
                    print(" test   - benchmarks the AI")
                    print("       options:")
                    print("     -a - advanced AI")
                    print("     -x - pits basic vs. advanced")
                    print(" clear  - unclogs the screen")
                elif "exit" in com:
                    print(" Exiting Program ...")
                    self.clear()
                    exit()
                elif "whoami" in com:
                    print(" username: "+self.player)
                elif "new" in com:
                    g = 0
                    com = com.removeprefix("new")
                    print(" Starting new game ...")
                    ai_name = "P2 [AI]"
                    scores = misc.ScoreManager(self.player,ai_name)
                    player_board = Board()
                    player_radar = Board()
                    ai_board = Board()
                    ai_radar = Board()
                    if "s" in com:
                        max_ai_guesses = 5
                        max_guesses = 5
                        game_mode = "Salvo"
                    else:
                        max_ai_guesses = 1
                        max_guesses = 1
                        game_mode = "Standard"
                    if "a" in com:
                        ai_level = "advanced"
                        ai_player = ai.AdvancedAI(ai_radar, player_board)
                    else:
                        ai_level = "basic"
                        ai_player = ai.BasicAI(ai_radar, player_board)
                    print(" Setting up AI board ...")
                    self.random_board(ai_board)
                    print(" Setting up your board ...")
                    if "c" in com:
                        self.state.set("Placing")    
                    else:
                        self.state.set("Game")
                        self.random_board(player_board)    
                    starting = randint(0,1)
                    turn = 1
                    if starting == 0:
                        print(" It's your turn")
                elif "test" in com:
                    if "x" in com:
                        self.matchup_ai()
                    else:
                        self.test_ai(com)
                elif "clear" in com:
                    self.clear()
                    print(" Main Menu")
                else:
                    print(" "+str(com)+" is an invalid or unrecognized command")
                    print(" type 'help' to list available commands")
            elif self.state.get() == "Placing":
                print(" This feature is not yet implemented")
                com = self.get_input("")
                if "help" in com:
                    print("    Available Commands:")
                    print(" help   - lists available commands")
                    print(" exit   - exits the program")
                    print(" whoami - displays your username")
                elif "exit" in com:
                    print(" Returning to Menu ...")
                    self.clear()
                    self.state.set("Main Menu")
                    print(welcome)
                    print(" "+self.state.get())
                elif "whoami" in com:
                    print(" username: "+player)
                else:
                    print(" "+str(com)+" is an invalid or unrecognized command")
                    print(" type 'help' to list available commands")
            elif self.state.get() == "Game":
                print(" Playing Area:")
                print(" Radar:")
                print(player_radar.display_board())
                print(" Ships:")
                print(player_board.display_board())
                #AI turn code
                t = turn % 2
                if t == starting:
                    print(" It is the AI's turn")
                    turn += 1
                    val = ai_player.guess(max_ai_guesses)
                    print(val)
                    if "Sunk" in val:
                        scores.inc_score(ai_name,1)
                        if game_mode == "Salvo":
                            max_guesses -= 1
                        if scores.get_score(ai_name) >= 5:
                            print(" You lost!")
                            print(" Your Ships:")
                            print(player_board.display_board())
                            print(" "+ai_name+"'s Ships:")
                            print(ai_board.display_board())
                            print(" Turns Played: "+str(turn))
                            print(" Game Mode: "+game_mode)
                            print(" AI Level: "+ai_level)
                            print(" Final Scores:")
                            print(" "+player+": "+str(scores.get_score(player)))
                            print(" "+ai_name+": "+str(scores.get_score(ai_name)))
                            self.state.set("Main Menu")
                            print("\n\n\n Main Menu")
                            continue
                    print(" It's your turn")
                    print(" Radar:")
                    print(player_radar.display_board())
                    print(" Ships:")
                    print(player_board.display_board())
                    g = 0
                com = self.get_input("")
                if "help" in com:
                    print("    Available Commands:")
                    print(" help   - lists available commands")
                    print(" exit   - exits the game")
                    print(" board  - displays the board")
                    print(" guess [row, col] - returns status of coordinates given")
                    print(" whoami - displays your username")
                    print(" info   - displays information about current game")
                    print(" pass   - skips your turn (useful for test the AI turn-by-turn)")
                elif "exit" in com:
                    print(" Exiting Game ...")
                    self.clear()
                    self.state.set("Main Menu")
                    print(welcome)
                    print(" "+self.state.get())
                elif "board" in com:
                    print(" Radar:")
                    print(player_radar.display_board())
                    print(" Ships:")
                    print(player_board.display_board())
                elif "guess" in com:
                    if com == "guess":
                        print(" guess cannot be used without parameters")
                        continue
                    com = com.removeprefix("guess")
                    valid_characters = {"a","b","c","d","e","f","g","h","i","j",}
                    valid_numbers = {"0","1","2","3","4","5","6","7","8","9"}
                    row = set()
                    col = set()
                    for c in com:
                        row.add(c)
                        col.add(c)
                    row = row.intersection(valid_characters)
                    col = col.intersection(valid_numbers)
                    if len(row) == 0 or len(col) == 0:
                        print(" guess requires two parameters, one in 0-9 and one in a-j")
                        continue
                    for x in row:
                        row = x
                        break
                    for x in col:
                        col = x
                        break
                    print(" You guessed: "+str(row).upper()+" "+str(col))
                    coords = ai_board.coords_from_input(row,col)
                    val = ai_board.guess(coords, player_radar)
                    print(val)
                    if "again" not in val:
                        if "Sunk" in val:
                            scores.inc_score(player, 1)
                            if game_mode == "Salvo":
                                max_ai_guesses -= 1
                            if scores.get_score(player) >= 5:
                                print(" Radar:")
                                print(player_radar.display_board())
                                print(" Ships:")
                                print(player_board.display_board())
                                print(" Turns Played: "+str(turn))
                                print(" Game Mode: "+game_mode)
                                print(" AI Level: "+ai_level)
                                print(" Final Scores:")
                                print(" "+player+": "+str(scores.get_score(player)))
                                print(" "+ai_name+": "+str(scores.get_score(ai_name)))
                                print(" Congratulations, "+player+"! You Won!")
                                self.state.set("Main Menu")
                                print("\n\n\n Main Menu")
                                continue
                        g += 1
                        if g >= max_guesses:
                            turn += 1                           
                elif "whoami" in com:
                    print(" username: "+self.player)
                elif "info" in com:
                    print(" Turn: "+str(turn))
                    print(" Game Mode: "+game_mode)
                    print(" AI Level: "+ai_level)
                    print(" Scores:")
                    print(" "+self.player+": "+str(scores.get_score(self.player)))
                    print(" "+ai_name+": "+str(scores.get_score(ai_name)))
                elif "pass" in com:
                    turn += 1
                else:
                    print(" "+str(com)+" is an invalid or unrecognized command")
                    print(" type 'help' to list available commands")
            else:
                print(" Unknown state error")
                print(" "+str(self.state.get())+" is an invalid state")
                self.state.set("Main Menu")
                print("\n Main Menu")

if __name__ == '__main__':
    game = BattleShipMain()
    game.loop()
    exit()
