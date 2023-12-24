
def update_stats(team, batting_stats, bowling_stats): # Function to update player stats after a match
    for player in team:
        player_name = player.name
        player.runs += batting_stats[player_name]['runs_scored']
        player.matches_played += 1
        if batting_stats[player_name]['dismissal_type'] is not None and batting_stats[player_name][
            'dismissed_by'] is not None:
            player.out += 1
        else:
            player.out += 0
        if batting_stats[player_name]['half_century']:
            player.half_centuries += 1
        if batting_stats[player_name]['half_century'] and batting_stats[player_name]['century']:
            player.centuries += 1
            player.half_centuries -= 1
        player.balls_faced += batting_stats[player_name]['balls_played']
        player.boundries['4s'] += batting_stats[player_name]['boundries']['4s']
        player.boundries['6s'] += batting_stats[player_name]['boundries']['6s']

        player.wickets_taken += bowling_stats[player_name]['wickets']
        player.overs_bowled += bowling_stats[player_name]['overs_bowled']
        player.runs_conceded += bowling_stats[player_name]['runs_conceded']