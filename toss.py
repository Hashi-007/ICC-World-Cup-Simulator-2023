import random





def toss(team1, team2):
    TOSS = ['heads', 'tails']
    # Random team will be chosen to pick the toss
    tossing_team = random.choice([team1, team2])
    toss_decision = random.choice(TOSS)
    # Access the 'name' attribute
    # print(f"{tossing_team.name} will choose to Toss")

    toss_result = random.choice(TOSS)

    if toss_decision == toss_result:
        # print(f"{tossing_team.name} has won the toss")
        # The team that wins the toss
        winning_team = tossing_team
        # Team that lost the toss
        losing_team = team1 if tossing_team == team2 else team2
        decision = random.choice(['bat', 'bowl'])


    else:
        # print(f"{tossing_team.name} has lost the toss")
        # The team that lost the toss
        losing_team = tossing_team
        # The team that wins the toss
        winning_team = team1 if tossing_team == team2 else team2
        decision = random.choice(['bat', 'bowl'])
        # print(f"Now {winning_team.name} will choose to Bat or Bowl")

    if decision == 'bat':
        # print(f"{winning_team.name} has chosen to bat first")
        # the batting team gets returned first
        return winning_team, losing_team, winning_team, decision
    else:
        # print(f"{winning_team.name} has chosen to bowl first")
        # the batting team gets returned first
        return losing_team, winning_team, winning_team, decision