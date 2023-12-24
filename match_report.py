class InningsReport:
    def __init__(self, runs, wickets ,batting_stats, bowling_stats,batting_team, bowling_team , overs ,fow, extras, data, rr_data):
        self.runs = runs
        self.wickets = wickets
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.batting_team_stats = batting_stats
        self.bowling_team_stats = bowling_stats
        self.overs = overs
        self.fall_of_wickets = fow
        self.extras = extras
        self.innings_data = data
        self.run_rate = rr_data


class Match:
    def __init__(self, innings1_report, innings2_report, winner, mov, toss, toss_d, stadium):
        self.innings1 = innings1_report
        self.innings2 = innings2_report
        self.winning_team = winner
        self.margin_of_victory = mov
        self.toss_winner = toss
        self.toss_decision = toss_d
        self.stadium = stadium



class MatchStorage:
    def __init__(self):
        self.matches = {}

    def add_match(self, team1, team2, match_id, match):
        print(f"Adding match: {team1.name} vs {team2.name} with ID {match_id}")
        self.matches[match_id] = {'team1': team1, 'team2': team2, 'match': match}

    def get_match(self, match_id):
        return self.matches.get(match_id, None)

    def get_match_id_by_object(self, match_obj):
        for match_id, match_info in self.matches.items():
            if match_info['match'] == match_obj:
                return match_id



WorldCup = MatchStorage()
