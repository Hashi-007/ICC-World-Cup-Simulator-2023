
def team_selection(team, batter_limit, bowler_limit, allrounder_limit): # Function that selects team lineup (11 players from a 15-man squad)

    top_order = []
    middle_order = []
    lower_order = []

    for player in team.players:
        if player.batting_position.main == 'top order':
            top_order.append(player)
        elif player.batting_position.main == 'middle order':
            middle_order.append(player)
        elif player.batting_position.main == 'lower order':
            lower_order.append(player)

    top_order = sorted(top_order, key=lambda x: (x.batting_position.sub, x.batting_skill, x.bowling_skill))
    middle_order = sorted(
        middle_order,
        key=lambda x: (
            x.batting_position.sub if x.batting_position.sub is not None else float('inf'),
            -x.batting_skill, -x.bowling_skill if x.role == 'Bowler' else -(
                    (x.batting_skill + x.bowling_skill) / 2)
        )
    )

    lower_order = sorted(lower_order, key=lambda x: x.batting_skill, reverse=True)

    selected_batters = []
    selected_all_rounders = []
    selected_bowlers = []

    for i in range(batter_limit):
        if len(top_order) == 1:
            player = top_order.pop(0)
            sub_position_selected = any(
                player1.batting_position.sub == p.batting_position.sub
                for p in selected_batters
            )
            if sub_position_selected is False:
                selected_batters.append(player)
                break
            else:
                break
        else:
            player1, player2 = top_order.pop(0), top_order.pop(0)
            if player1.batting_position.sub < player2.batting_position.sub:
                sub_position_selected = any(
                    player1.batting_position.sub == p.batting_position.sub
                    for p in selected_batters
                )

                if sub_position_selected is False:
                    selected_batters.append(player1)
                    top_order.append(player2)


                else:
                    selected_batters.append(player2)
                    top_order.append(player1)

            elif player1.batting_position.sub > player2.batting_position.sub:
                sub_position_selected = any(
                    player1.batting_position.sub == p.batting_position.sub
                    for p in selected_batters
                )

                if sub_position_selected is False:
                    selected_batters.append(player2)
                    top_order.append(player1)

                else:
                    selected_batters.append(player1)
                    top_order.append(player2)




            elif player1.batting_position.sub == player2.batting_position.sub:
                if player1.batting_skill > player2.batting_skill:
                    selected_batters.append(player1)
                    top_order.append(player2)

                else:
                    selected_batters.append(player2)
                    top_order.append(player1)

    middle_bat = []
    middle_all = []

    for player in middle_order:
        if player.role == 'Batsman':
            middle_bat.append(player)
        elif player.role == 'All-Rounder':
            middle_all.append(player)

    for i in range(batter_limit - len(selected_batters)):
        if len(middle_bat) == 1 and len(selected_batters) < batter_limit:
            a = middle_bat.pop()
            selected_batters.append(a)
        else:
            a, b = middle_bat[0], middle_bat[1]
            if a.batting_skill > b.batting_skill:
                a1 = middle_bat.pop(0)
                selected_batters.append(a1)
            else:
                a1 = middle_bat.pop(1)
                selected_batters.append(a1)

    for i in range(allrounder_limit):

        if len(selected_all_rounders) == allrounder_limit:
            break

        if len(middle_all) == 1 and len(selected_all_rounders) < allrounder_limit:
            all_rounder = middle_all.pop()
            selected_all_rounders.append(all_rounder)
        else:
            a, b = middle_all[0], middle_all[1]
            if ((a.batting_skill + a.bowling_skill) / 2) > ((b.batting_skill + b.bowling_skill) / 2):
                a1 = middle_all.pop(0)
                selected_all_rounders.append(a1)
            else:
                a1 = middle_all.pop(1)
                selected_all_rounders.append(a1)

    for i in range(bowler_limit):
        if len(lower_order) == 1 and len(selected_bowlers) < bowler_limit:
            a = lower_order.pop()
            selected_bowlers.append(a)
        else:
            a, b = lower_order[0], lower_order[1]
            if a.bowling_skill > b.bowling_skill:
                a1 = lower_order.pop(0)
                selected_bowlers.append(a1)
            else:
                a1 = lower_order.pop(1)
                selected_bowlers.append(a1)

    selected_team = selected_batters + selected_all_rounders + selected_bowlers

    return selected_team