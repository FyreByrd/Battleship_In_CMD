from player import Player, AIPlayer, StupidAI, BasicAI, AdvancedAI
from scratch import FastAdvancedAI
import time
from datetime import timedelta

types = {
    "s": StupidAI,
    "b": BasicAI,
    "a": AdvancedAI,
    "f": FastAdvancedAI
}

p = [1, 1, 10, 100, 1000, 10000, 100000]

def test(args):
    args = args.split()
    solo = args[0] == "s"
    ai = types[args[1]]()
    opp = AIPlayer()
    iter = 0
    m = 0
    if not solo:
        opp = types[args[2]]()
        iter = 10 ** int(args[3])
        m = p[int(args[3])]
    else:
        iter = 10 ** int(args[2])
        m = p[int(args[2])]
    t_start = time.time()
    if solo:
        s1 = s2 = s3 = s4 = s5 = 0
        m1 = m2 = m3 = m4 = m5 = 100
        x1 = x2 = x3 = x4 = x5 = 0
        print(ai.name)
        for i in range(iter):
            j = 0
            score = 0
            if (i + 1) % m == 0:
                print(i+1)
            while score < 5:
                j += 1
                t = ai.turn(opp)
                if "Sunk" in t[0]:
                    score += 1 
                    if score == 1:
                        s1 += j
                        m1 = m1 if j >= m1 else j
                        x1 = x1 if j <= x1 else j
                    elif score == 2:
                        s2 += j
                        m2 = m2 if j >= m2 else j
                        x2 = x2 if j <= x2 else j
                    elif score == 3:
                        s3 += j
                        m3 = m3 if j >= m3 else j
                        x3 = x3 if j <= x3 else j
                    elif score == 4:
                        s4 += j
                        m4 = m4 if j >= m4 else j
                        x4 = x4 if j <= x4 else j
                    elif score == 5:
                        s5 += j
                        m5 = m5 if j >= m5 else j
                        x5 = x5 if j <= x5 else j
            ai.clear_state()
            opp.new_board()
        t_full = time.time() - t_start
        d = timedelta(seconds = t_full)
        print("### "+ai.name)
        print("Iterations: "+str(iter))
        print("Time:       "+str(d)+" ("+str(t_full)+")")
        print("|             | Mean  | Range    |")
        print("|---          |:-:    |:-:       |")
        print("| First Sunk  | "+str(s1/iter)+" | ["+str(m1)+", "+str(x1)+"] |")
        print("| Second Sunk | "+str(s2/iter)+" | ["+str(m2)+", "+str(x2)+"] |")
        print("| Third Sunk  | "+str(s3/iter)+" | ["+str(m3)+", "+str(x3)+"] |")
        print("| Fourth Sunk | "+str(s4/iter)+" | ["+str(m4)+", "+str(x4)+"] |")
        print("| Gameover    | "+str(s5/iter)+" | ["+str(m5)+", "+str(x5)+"] |")
