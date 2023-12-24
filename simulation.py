from Probabilities import calc_adjusted_prob
import random
from collections import deque
from Probabilities import calc_dynamic_field_probability, calc_dynamic_runout


def sim_ball(bowler, striker, pitch): # Simulation of ball


    adjusted_weights = calc_adjusted_prob(striker.batting_skill, bowler.bowling_skill, pitch)
    ball_outcome = random.choices([0, 1, 2, 3, 4, 6, 'W', 'extra'], [adjusted_weights['dot'],
                                                                     adjusted_weights['1'],
                                                                     adjusted_weights['2'],
                                                                     adjusted_weights['3'],
                                                                     adjusted_weights['4'],
                                                                     adjusted_weights['6'],
                                                                     adjusted_weights['W'],
                                                                     adjusted_weights['extra']])[0]

    return ball_outcome


def sim_over(bowler, team_runs, team_wickets, striking_batsman, rear_batsman, data, target, overs_bowled, batting_stats,
             bowling_stats, fow, extras, batting_order, bowling_team, pitch): # Simulation of an over
    overs_bowled = int(overs_bowled)
    balls_bowled_in_over = 0
    free_hit = False
    if target:
        if team_wickets >= 10 or team_runs >= target:
            return team_runs, team_wickets, striking_batsman, rear_batsman
    elif team_wickets >= 10:
        return team_runs, team_wickets, striking_batsman, rear_batsman

    current_over = []
    for ball in range(7):

        if balls_bowled_in_over >= 6:
            break

        if team_wickets >= 10:
            break

        if target:
            if team_runs >= target:
                break

        ball_outcome = sim_ball(bowler, striking_batsman, pitch)

        if ball_outcome in [0, 1, 2, 3, 4, 6]:
            ball_data = {
                'bowler': bowler.name,
                'striking_batsman': striking_batsman.name,
                'outcome': ball_outcome
            }
            current_over.append(ball_data)
            team_runs += ball_outcome
            batting_stats[striking_batsman.name]['runs_scored'] += ball_outcome
            batting_stats[striking_batsman.name]['balls_played'] += 1
            bowling_stats[bowler.name]['runs_conceded'] += ball_outcome
            balls_bowled_in_over += 1
            if batting_stats[striking_batsman.name]['runs_scored'] >= 50:
                batting_stats[striking_batsman.name]['half_century'] = True
            if batting_stats[striking_batsman.name]['runs_scored'] >= 100:
                batting_stats[striking_batsman.name]['century'] = True

            if ball_outcome in [1, 3]:
                striking_batsman, rear_batsman = rear_batsman, striking_batsman

            elif ball_outcome in [4, 6]:
                batting_stats[striking_batsman.name]['boundries'][str(ball_outcome) + 's'] += 1

        if free_hit:
            ball_outcome = sim_ball(bowler, striking_batsman, pitch)
            if ball_outcome not in ['W', 'extra']:
                team_runs += ball_outcome
                balls_bowled_in_over += 1
                batting_stats[striking_batsman.name]['runs_scored'] += ball_outcome
                batting_stats[striking_batsman.name]['balls_played'] += 1
                bowling_stats[bowler.name]['runs_conceded'] += ball_outcome
                free_hit = False
                ball_data = {
                    'bowler': bowler.name,
                    'striking_batsman': striking_batsman.name,
                    'outcome': ball_outcome
                }
                current_over.append(ball_data)


        else:
            if ball_outcome == 'W':
                balls_bowled_in_over += 1

                if bowler.bowling_type == 'Pace':
                    Wicket = random.choice(['Bowled', 'Caught', 'LBW', 'Run Out'])
                else:
                    Wicket = random.choice(['Bowled', 'Caught', 'LBW', 'Stumped', 'Run Out'])
                batting_stats[striking_batsman.name]['balls_played'] += 1
                if Wicket in ['Bowled', 'LBW', 'Stumped']:
                    team_wickets += 1
                    fow[team_wickets] = f'{team_runs}-{team_wickets}'
                    bowling_stats[bowler.name]['wickets'] += 1
                    batting_stats[striking_batsman.name]['dismissal_type'] = Wicket
                    batting_stats[striking_batsman.name]['dismissed_by'] = bowler.name
                    ball_data = {
                        'bowler': bowler.name,
                        'striking_batsman': striking_batsman.name,
                        'outcome': Wicket
                    }
                    current_over.append(ball_data)

                    if batting_order:
                        striking_batsman = batting_order.popleft()

                    if team_wickets >= 10:
                        break

                if Wicket in ['Caught']:
                    fielder = random.choice(bowling_team)
                    adjusted_catch_weights = calc_dynamic_field_probability(fielder.fielding_skill)
                    catch_outcome = random.choices(['Caught', 'Dropped'], [adjusted_catch_weights['Caught'],
                                                                           adjusted_catch_weights['Dropped']])[
                        0]

                    ball_data = {
                        'bowler': bowler.name,
                        'striking_batsman': striking_batsman.name,
                        'outcome': catch_outcome
                    }
                    current_over.append(ball_data)

                    if catch_outcome == 'Caught':
                        batting_stats[striking_batsman.name]['dismissal_type'] = Wicket
                        batting_stats[striking_batsman.name]['dismissed_by'] = bowler.name
                        batting_stats[striking_batsman.name]['fielder'] = fielder.name
                        bowling_stats[bowler.name]['wickets'] += 1
                        team_wickets += 1
                        fow[team_wickets] = f'{team_runs}-{team_wickets}'

                        if batting_order:
                            striking_batsman = batting_order.popleft()

                        if team_wickets >= 10:
                            break

                    elif catch_outcome == 'Dropped':

                        batting_stats[striking_batsman.name]['dismissal_type'] = None
                        batting_stats[striking_batsman.name]['dismissed_by'] = None


                elif Wicket in ['Run Out']:

                    fielder = random.choice(bowling_team)
                    adjusted_runout_weights = calc_dynamic_runout(fielder.fielding_skill)
                    runout_outcome = \
                        random.choices(['Direct Hit', 'Missed'], [adjusted_runout_weights['Direct Hit'],
                                                                  adjusted_runout_weights['Missed']])[0]

                    ball_data = {
                        'bowler': bowler.name,
                        'striking_batsman': striking_batsman.name,
                        'outcome': runout_outcome
                    }
                    current_over.append(ball_data)

                    if runout_outcome == 'Direct Hit':
                        batting_stats[striking_batsman.name]['dismissal_type'] = Wicket
                        batting_stats[striking_batsman.name]['dismissed_by'] = fielder.name
                        team_wickets += 1
                        fow[team_wickets] = f'{team_runs}-{team_wickets}'

                        if batting_order:
                            striking_batsman = batting_order.popleft()

                        if team_wickets >= 10:
                            break
                    elif runout_outcome == 'Missed':

                        batting_stats[striking_batsman.name]['dismissal_type'] = None
                        batting_stats[striking_batsman.name]['dismissed_by'] = None

        if ball_outcome == 'extra':

            team_runs += 1
            extra = random.choice(['Wide', 'No Ball'])
            ball_data = {
                'bowler': bowler.name,
                'striking_batsman': striking_batsman.name,
                'outcome': extra
            }
            current_over.append(ball_data)
            extras[extra] += 1
            bowling_stats[bowler.name]['runs_conceded'] += 1
            if extra == 'No Ball':
                free_hit = True

    if balls_bowled_in_over >= 6:
        over = overs_bowled
    else:
        over = float(f'{overs_bowled - 1}.{balls_bowled_in_over}')

    return team_runs, team_wickets, striking_batsman, rear_batsman, current_over, over


def sim_innings(batting_team, bowling_team, pitch ,target=None): # Simulation of Innings
    innings_data = []
    fall_of_wickets = {1 : '', 2 : '', 3 : '', 4 : '', 5 : '', 6 : '', 7 : '', 8 : '', 9 : '', 10 : '' }
    extras = {'Wide' : 0, 'No Ball' : 0}
    team_runs = 0
    team_wickets = 0
    overs_bowled = 0
    run_rate = {}

    # Create dictionaries to track runs and balls faced for each batsman
    batting_stats = {batter.name: {'runs_scored' : 0, 'balls_played' : 0, 'dismissal_type' : None,
                                   'dismissed_by' : None, 'fielder' : None, 'boundries' : {'4s' : 0, '6s' : 0 }, 'century' : False,
                                   'half_century' : False} for batter in batting_team}
    bowling_stats = {bowler.name: {'wickets' : 0, 'runs_conceded' : 0, 'overs_bowled' : 0, 'economy' : 0} for bowler in bowling_team}
    batting_order = deque(batting_team.copy())
    bowling_order = deque(sorted(bowling_team, key=lambda x: x.bowling_skill, reverse=True))

    striking_batsman = batting_order.popleft()
    rear_batsman = batting_order.popleft()

    pair1 = deque()
    pair2 = deque()
    pair3 = deque()

    while len(bowling_order) >= 2 and len(pair1) < 2:
        pair1.append(bowling_order.popleft())

    while len(bowling_order) >= 2 and len(pair2) < 2:
        pair2.append(bowling_order.popleft())

    while len(bowling_order) >= 2 and len(pair3) < 2:
        pair3.append(bowling_order.popleft())

    pairs = deque([pair1, pair2, pair3])

    while team_wickets < 10 and overs_bowled < 50:

        if overs_bowled % 1 != 0:
            current_bowler = pairs[0][int(overs_bowled+1) % 2]
        else:
            current_bowler = pairs[0][overs_bowled % 2]
        if bowling_stats[current_bowler.name]['overs_bowled'] == 10:
            pairs.rotate(-1)

            if overs_bowled % 1 != 0:
                current_bowler = pairs[0][int(overs_bowled + 1) % 2]
            else:
                current_bowler = pairs[0][overs_bowled % 2]

        team_runs, team_wickets, striking_batsman, rear_batsman, data, overs_bowled = \
            sim_over(current_bowler, team_runs, team_wickets, striking_batsman, rear_batsman, innings_data, target, overs_bowled, batting_stats, bowling_stats, fall_of_wickets, extras, batting_order, bowling_team, pitch)
        run_rate[overs_bowled] = {'total_runs': team_runs, 'team_wickets': team_wickets}
        innings_data.append(data)
        striking_batsman, rear_batsman = rear_batsman, striking_batsman
        overs_bowled += 1

        bowling_stats[current_bowler.name]['overs_bowled'] += 1

        if overs_bowled % 10 == 0:
            pairs.rotate(-1)
            pairs = deque(p for p in pairs if p != pair1)

        if overs_bowled == 40:
            pairs.appendleft(pair1)

        if target is not None and team_runs >= target:
            break

        bowling_stats[current_bowler.name]['economy'] = bowling_stats[current_bowler.name]['runs_conceded'] / bowling_stats[current_bowler.name]['overs_bowled']

    return team_runs, team_wickets, overs_bowled, batting_stats, bowling_stats, fall_of_wickets, extras, innings_data, run_rate