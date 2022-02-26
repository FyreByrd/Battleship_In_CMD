#player.py: contains class definitions for various types of players
#author: Aidan Jones
#AI algorithms are based off of: https://www.datagenetics.com/blog/december32011/

#<<<<<Class Definitions>>>>>
#--base class for player
class Player():
    #--constructor
    def __init__(this,name:str):
        this.name = name
        this.score = 0
    #--str conversion method
    def __str__(this):
        return this.name
    #--method to take a turn
    def turn(this):
        raise NotImplementedError
#--class for basic human player
class HumanPlayer(Player):
    #--constructor
    def __init__(this, name:str):
        super().__init__(name)
#--class for a human opponent playing through the internet
#class WebPlayer(HumanPlayer):
#    pass
#--base class for an AI player
class AIPlayer(Player):
    pass
#--AI that uses a PRNG to exhaust the board
class StupidAI(AIPlayer):
    pass
#--AI that uses a basic 2-stage Hunt/Target algorithm
class BasicAI(AIPlayer):
    pass
#--AI that uses a Probability Density Function to aid a 2-stage Hunt/Target algorithm
class AdvancedAI(AIPlayer):
    pass
