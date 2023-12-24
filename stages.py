from extract_data import teams
from match import sim_match
import random, itertools
from stadium import stadiums


def group_stage(teams): # Function to simulate the Group Stage
    team_pairs = sorted(list(itertools.combinations(teams, 2)), key=lambda x: random.random())

    for number, match in enumerate(team_pairs, start=1):
        team1, team2 = match
        match_id = f"Match#{number}"
        sim_match(team1, team2, match_id ,random.choice(stadiums))

def player_stats(): # Function to return lists with the best performing players
    players = []
    players_with_nonzero_economy = []
    players_with_nonzero_bat_avg = []
    for team in teams:
        for player in team.players:
            if player.matches_played >= 4:
                players.append(player)
                if player.calc_economy() > 0:
                    players_with_nonzero_economy.append(player)
                if player.calc_bat_avg() > 0:
                    players_with_nonzero_bat_avg.append(player)

    top_scorers = sorted(players, key=lambda x: x.runs, reverse=True)[:5]
    top_wicket_takers = sorted(players, key=lambda x: x.wickets_taken, reverse=True)[:5]
    top_economy = sorted(players_with_nonzero_economy, key=lambda x: x.calc_economy())[:5]
    top_50s = sorted(players, key=lambda x: x.half_centuries, reverse=True)[:5]
    top_100s = sorted(players, key=lambda x: x.centuries, reverse=True)[:5]
    top_bat_avg = sorted(players_with_nonzero_bat_avg, key=lambda x: x.calc_bat_avg(), reverse=True)[:5]

    return top_scorers, top_wicket_takers, top_economy, top_50s, top_100s, top_bat_avg

def finals(team1, team2, id): # Function to simulate the semifinals and final
    initial_matches_won_team1 = team1.matches_won
    initial_matches_won_team2 = team2.matches_won

    #print(f"\n\nSemiFinal: {team1.name} VS {team2.name}")
    teamA,teamA_runs,teamA_wickets,teamA_overs,teamB, teamB_runs, teamB_wickets, teamB_overs = sim_match(team1, team2, id ,random.choice(stadiums))

    if team1.name == teamA and team2.name == teamB:
        team1_runs = teamA_runs
        team1_overs = teamA_overs
        team1_wickets = teamA_wickets

        team2_runs = teamB_runs
        team2_wickets = teamB_wickets
        team2_overs = teamB_overs

    elif team1.name == teamB and team2.name == teamA:
        team1_runs = teamB_runs
        team1_wickets = teamB_wickets
        team1_overs = teamB_overs

        team2_runs = teamA_runs
        team2_wickets = teamA_wickets
        team2_overs = teamA_overs

    if team1.matches_won > initial_matches_won_team1:
        winner = team1
    elif team2.matches_won > initial_matches_won_team2:
        winner = team2

    return winner, team1_runs, team1_wickets, team1_overs, team2_runs, team2_wickets, team2_overs