class StateManager:
    def __init__(self, state):
        self.state = state
    def get(self):
        return self.state
    def set(self, value):
        self.state = value
class ScoreManager:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.score1 = 0
        self.player2 = player2
        self.score2 = 0
    def get_score(self, player):
        if player == self.player1:
            return self.score1
        elif player == self.player2:
            return self.score2
        else:
            return -1
    def inc_score(self, player, amt=1):
        if player == self.player1:
            self.score1 += amt
            return self.score1
        elif player == self.player2:
            self.score2 += amt
            return self.score2
        else:
            return -2
            