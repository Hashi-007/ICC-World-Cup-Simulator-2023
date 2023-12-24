class Player:
    def __init__(self, name, role, batting_skill, batting_type, bowling_skill, bowl_type, fielding_skill):
        self.name = name
        self.role = role
        self.batting_skill = batting_skill
        self.batting_position = batting_type
        self.bowling_skill = bowling_skill
        self.bowling_type = bowl_type
        self.fielding_skill = fielding_skill
        self.runs = 0
        self.out = 0
        self.boundries = {'4s' : 0, '6s': 0}
        self.balls_faced = 0
        self.wickets_taken = 0
        self.overs_bowled = 0
        self.centuries = 0
        self.half_centuries = 0
        self.runs_conceded = 0
        self.matches_played = 0



    def calc_economy(self):
        if self.runs_conceded != 0 and self.overs_bowled != 0:
            economy = self.runs_conceded / self.overs_bowled
            return economy
        else:
            return 0

    def calc_bat_avg(self):
        if self.runs != 0 and self.matches_played != 0:
            if self.out == 0:
                return self.runs
            else:
                batting_avg = self.runs / self.out
                return batting_avg
        else:
            return 0



class Batting_Position:
    def __init__(self, main, sub=None):
        self.main = main
        self.sub = sub
