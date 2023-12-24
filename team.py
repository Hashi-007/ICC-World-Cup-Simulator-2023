class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.matches_played = 0
        self.matches_won = 0
        self.matches_lost = 0
        self.points = 0
        self.NRR = 0
        self.runs_foward = 0
        self.overs_batted = 0
        self.runs_against = 0
        self.overs_bowled = 0

    def calc_nrr(self):
        if self.overs_batted > 0 and self.overs_bowled > 0:
            foward_rr = self.runs_foward / self.overs_batted
            against_rr = self.runs_against / self.overs_bowled
            self.NRR = foward_rr - against_rr
        else:
            pass

    def add_player(self, player):
        self.players.append(player)
