from toss import toss
from update_stats import update_stats
from team_selection import team_selection
from simulation import sim_innings
from match_report import InningsReport, Match, WorldCup
def sim_match(team1, team2, match_id ,stadium): # Simulation of a Cricket Match
    pitch = stadium.pitch_type

    batting_team, bowling_team, toss_winner, toss_decision = toss(team1, team2)

    if pitch.pitch_type.value == "Batting Pitch":
        batter_limit = 5
        bowler_limit = 4
        all_rounder_limit = 2

    elif pitch.pitch_type.value == 'Bowling Pitch':
        batter_limit = 4
        bowler_limit = 4
        all_rounder_limit = 3

    else:
        batter_limit = 5
        bowler_limit = 3
        all_rounder_limit = 3


    selected_batting_team = team_selection(batting_team, batter_limit, bowler_limit, all_rounder_limit)
    selected_bowling_team = team_selection(bowling_team, batter_limit, bowler_limit, all_rounder_limit)

    innings1Data = []
    innings2Data = []
    team1_runs, team1_wickets, overs1, bat_stats1, bowl_stats1, fall_of_wickets1, extras1, innings1Data, runrate1 = sim_innings(selected_batting_team, selected_bowling_team, pitch)

    innings1 = InningsReport(team1_runs, team1_wickets, bat_stats1, bowl_stats1, batting_team, bowling_team ,overs1, fall_of_wickets1, extras1, innings1Data, runrate1)

    print(f"{batting_team.name}: {team1_runs}/{team1_wickets} in {overs1} Overs")

    if team1_wickets == 10:
        overs1_nrr = 50
    else:
        overs1_nrr = overs1

    target = team1_runs + 1

    batting_team, bowling_team = bowling_team, batting_team
    selected_batting_team, selected_bowling_team = selected_bowling_team, selected_batting_team
    team2_runs, team2_wickets, overs2, bat_stats2, bowl_stats2, fall_of_wickets2, extras2, innings2Data, runrate2 = sim_innings(selected_batting_team,
                                                                             selected_bowling_team, pitch ,target)

    innings2 = InningsReport(team2_runs, team2_wickets, bat_stats2, bowl_stats2, batting_team, bowling_team ,overs2, fall_of_wickets2, extras2, innings2Data, runrate2)

    print(f"{batting_team.name}: {team2_runs}/{team2_wickets} in {overs2} Overs")

    if team2_wickets == 10:
        overs2_nrr = 50
    else:
        overs2_nrr = overs2


    if team2_runs >= target:
        print(f"\n{batting_team.name} won by {10 - team2_wickets} wickets!\n")
        if team2.name == batting_team.name and team1.name == bowling_team.name:
            team2.matches_played += 1
            team2.matches_won += 1
            team2.points += 2
            team2.runs_foward += team2_runs
            team2.overs_batted += overs2_nrr
            team2.runs_against += team1_runs
            team2.overs_bowled += overs1_nrr

            team1.matches_played += 1
            team1.matches_lost += 1
            team1.runs_foward += team1_runs
            team1.overs_batted += overs1_nrr
            team1.runs_against += team2_runs
            team1.overs_bowled += overs2_nrr

            match = Match(innings1, innings2, team2, f"{batting_team.name} won by {10 - team2_wickets} wickets!", toss_winner, toss_decision, stadium)


            update_stats(selected_batting_team, bat_stats2, bowl_stats1)

            update_stats(selected_bowling_team, bat_stats1, bowl_stats2)

        elif team1.name == batting_team.name and team2.name == bowling_team.name:
            team1.points += 2

            team2.matches_played += 1
            team2.matches_lost += 1
            team2.runs_foward += team1_runs
            team2.overs_batted += overs1_nrr
            team2.runs_against += team2_runs
            team2.overs_bowled += overs2_nrr

            team1.matches_played += 1
            team1.matches_won += 1
            team1.runs_foward += team2_runs
            team1.overs_batted += overs2_nrr
            team1.runs_against += team1_runs
            team1.overs_bowled += overs1_nrr


            match = Match(innings1, innings2, team1, f"{batting_team.name} won by {10 - team2_wickets} wickets!",toss_winner, toss_decision, stadium)


            update_stats(selected_bowling_team, bat_stats1, bowl_stats2)

            update_stats(selected_batting_team, bat_stats2, bowl_stats1)

    else:
        print(f"\n{bowling_team.name} won by {team1_runs - team2_runs} runs!\n")
        if team2.name == bowling_team.name and team1.name == batting_team.name:
            team2.points += 2
            team2.matches_played += 1
            team2.matches_won += 1
            team2.runs_foward += team1_runs
            team2.overs_batted += overs1_nrr
            team2.runs_against += team2_runs
            team2.overs_bowled += overs2_nrr

            team1.matches_played +=1
            team1.matches_lost += 1
            team1.runs_foward += team2_runs
            team1.overs_batted += overs2_nrr
            team1.runs_against += team1_runs
            team1.overs_bowled += overs1_nrr

            match = Match(innings1, innings2, team2, f"{bowling_team.name} won by {team1_runs - team2_runs} runs!", toss_winner, toss_decision, stadium)


            update_stats(selected_bowling_team, bat_stats1, bowl_stats2)

            update_stats(selected_batting_team, bat_stats2, bowl_stats1)

        elif team1.name == bowling_team.name and team2.name == batting_team.name:
            team1.points += 2

            team2.matches_played += 1
            team2.matches_lost += 1
            team2.runs_foward += team2_runs
            team2.overs_batted += overs2_nrr
            team2.runs_against += team1_runs
            team2.overs_bowled += overs1_nrr

            team1.matches_played += 1
            team1.matches_won += 1
            team1.runs_foward += team1_runs
            team1.overs_batted += overs1_nrr
            team1.runs_against += team2_runs
            team1.overs_bowled += overs2_nrr

            match = Match(innings1, innings2, team1, f"{bowling_team.name} won by {team1_runs - team2_runs} runs!", toss_winner, toss_decision, stadium)

            update_stats(selected_batting_team, bat_stats2, bowl_stats1)

            update_stats(selected_bowling_team, bat_stats1, bowl_stats2)

    WorldCup.add_match(team1, team2, match_id, match)


    return bowling_team.name,team1_runs, team1_wickets, overs1, batting_team.name ,team2_runs, team2_wickets, overs2