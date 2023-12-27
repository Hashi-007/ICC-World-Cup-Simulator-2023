import random

def calc_adjusted_prob(batsman_skill, bowler_skill, pitch):
    try:
        ball_probabilities = pitch.base_probabilities

        adjusted_probability = ball_probabilities.copy()

        ball_length = ['Bouncer', 'Short length', 'Good length', 'Full length', 'Yorker']
        bouncer_prob = {'bouncer': 0.85, 'high': 0.05, 'short': 0.1}
        shortLength_prob = {'short': 1}
        goodLength_prob = {'good_length': 0.25, 'half_volley': 0.4, 'slot': 0.35}
        fullLength = {'full': 0.40, 'slot': 0.35, 'over_pitched': 0.25}
        yorker_prob = {'yorker': 0.17, 'slot': 0.43, 'full_toss': 0.4}

        bowler_length = random.choice(ball_length)

        if bowler_length == 'Bouncer':
            bouncer_prob['bouncer'] += (bowler_skill - 50) * 0.001
            bouncer_prob['high'] -= (bowler_skill - 40) * 0.001

            total = sum(bouncer_prob.values())
            for key in bouncer_prob.keys():
                bouncer_prob[key] /= total

            length = random.choices(['bouncer', 'high', 'short'], [bouncer_prob['bouncer'],
                                                                   bouncer_prob['high'],
                                                                   bouncer_prob['short']])[0]

            if length == 'bouncer':

                adjusted_probability['6'] += (batsman_skill - 50) * 0.001
                adjusted_probability['4'] += (batsman_skill - 50) * 0.001
                adjusted_probability['W'] -= (batsman_skill - 50) * 0.001

                adjusted_probability['W'] += (bowler_skill - 50) * 0.002
                adjusted_probability['4'] -= (bowler_skill - 50) * 0.001
                adjusted_probability['6'] -= (bowler_skill - 50) * 0.001
                adjusted_probability['dot'] += (bowler_skill - 50) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

            elif length == 'high':
                adjusted_probability['extra'] = 1
                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob

                return adjusted_probability

            elif length == 'short':
                adjusted_probability['4'] += (batsman_skill - 45) * 0.001
                adjusted_probability['6'] += (batsman_skill - 45) * 0.001

                adjusted_probability['dot'] += (bowler_skill - 55) * 0.001
                adjusted_probability['W'] += (bowler_skill - 60) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

        elif bowler_length == 'Good length':
            goodLength_prob['good_length'] += (bowler_skill - 55) * 0.001
            goodLength_prob['half_volley'] -= (bowler_skill - 40) * 0.001
            goodLength_prob['slot'] -= (bowler_skill - 40) * 0.001

            total = sum(goodLength_prob.values())
            for key in goodLength_prob.keys():
                goodLength_prob[key] /= total

            length = random.choices(['good_length', 'slot', 'half-volley'], [goodLength_prob['good_length'],
                                                                             goodLength_prob['slot'],
                                                                             goodLength_prob[
                                                                                 'half_volley']])[0]

            if length == 'good_length':
                adjusted_probability['W'] += (bowler_skill - 45) * 0.001
                adjusted_probability['dot'] += (bowler_skill - 45) * 0.001

                adjusted_probability['6'] += (batsman_skill - 60) * 0.001
                adjusted_probability['4'] += (batsman_skill - 55) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

            elif length == 'slot':
                adjusted_probability['6'] += (batsman_skill - 40) * 0.001
                adjusted_probability['4'] += (batsman_skill - 40) * 0.001
                adjusted_probability['W'] -= (batsman_skill - 50) * 0.001
                adjusted_probability['dot'] -= (batsman_skill - 45) * 0.001

                adjusted_probability['dot'] += (bowler_skill - 60) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

            elif length == 'half-volley':
                adjusted_probability['4'] += (batsman_skill - 40) * 0.001
                adjusted_probability['2'] += (batsman_skill - 40) * 0.001

                adjusted_probability['6'] += (100 - bowler_skill) * 0.001
                adjusted_probability['dot'] += (bowler_skill - 60) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

        elif bowler_length == 'Full length':
            fullLength['full'] += (bowler_skill - 50) * 0.001
            fullLength['slot'] -= (bowler_skill - 50) * 0.001
            fullLength['over_pitched'] -= (bowler_skill - 50) * 0.001

            total = sum(fullLength.values())
            for key in fullLength.keys():
                fullLength[key] /= total

            length = random.choices(['full_length', 'slot', 'over_pitched'], [fullLength['full'],
                                                                              fullLength['slot'],
                                                                              fullLength['over_pitched']])[0]

            if length == 'full_length':
                adjusted_probability['W'] += (bowler_skill - 50) * 0.001
                adjusted_probability['dot'] += (bowler_skill - 50) * 0.01

                adjusted_probability['4'] += (batsman_skill - 50) * 0.001
                adjusted_probability['1'] += (batsman_skill - 40) * 0.001
                adjusted_probability['2'] += (batsman_skill - 40) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

            elif length == 'slot':
                adjusted_probability['6'] += (batsman_skill - 40) * 0.001
                adjusted_probability['4'] += (batsman_skill - 40) * 0.001
                adjusted_probability['W'] -= (batsman_skill - 40) * 0.001
                adjusted_probability['dot'] -= (batsman_skill - 45) * 0.001

                adjusted_probability['dot'] += (bowler_skill - 60) * 0.001
                adjusted_probability['W'] += (100 - bowler_skill) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

            elif length == 'over_pitched':
                adjusted_probability['4'] += (batsman_skill - 50) * 0.001
                adjusted_probability['dot'] -= (batsman_skill - 50) * 0.001
                adjusted_probability['W'] -= (batsman_skill - 45) * 0.001

                adjusted_probability['6'] += (100 - bowler_skill) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability


        elif bowler_length == 'Yorker':
            yorker_prob['yorker'] += (bowler_skill - 65) * 0.001

            total = sum(yorker_prob.values())
            for key in yorker_prob.keys():
                yorker_prob[key] /= total

            length = random.choices(['yorker', 'slot', 'full_toss'], [yorker_prob['yorker'],
                                                                      yorker_prob['slot'],
                                                                      yorker_prob['full_toss']])[0]

            if length == 'yorker':
                adjusted_probability['W'] += (bowler_skill - 45) * 0.001
                adjusted_probability['dot'] += (bowler_skill - 30) * 0.001

                adjusted_probability['W'] -= (batsman_skill - 65) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

            elif length == 'slot':
                adjusted_probability['6'] += (batsman_skill - 40) * 0.001
                adjusted_probability['4'] += (batsman_skill - 40) * 0.001
                adjusted_probability['W'] -= (100 - batsman_skill) * 0.001
                adjusted_probability['dot'] -= (batsman_skill - 45) * 0.001

                adjusted_probability['dot'] += (bowler_skill - 60) * 0.001
                adjusted_probability['W'] += (100 - bowler_skill) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

            elif length == 'full_toss':
                adjusted_probability['6'] += (batsman_skill - 40) * 0.001
                adjusted_probability['4'] += (batsman_skill - 35) * 0.001

                adjusted_probability['W'] += (batsman_skill - 55) * 0.001

                total_prob = sum(adjusted_probability.values())
                for key in adjusted_probability:
                    adjusted_probability[key] /= total_prob
                return adjusted_probability

        elif bowler_length == 'Short length':
            length = 'short'
            adjusted_probability['dot'] -= (batsman_skill - 50) * 0.001
            adjusted_probability['1'] += (batsman_skill - 50) * 0.002
            adjusted_probability['2'] += (batsman_skill - 50) * 0.001
            adjusted_probability['3'] += (batsman_skill - 50) * 0.001
            adjusted_probability['4'] += (batsman_skill - 50) * 0.003
            adjusted_probability['6'] += (batsman_skill - 50) * 0.001
            adjusted_probability['W'] -= (batsman_skill - 50) * 0.002

            # Adjustment based on bowler skill
            adjusted_probability['dot'] += (bowler_skill - 50) * 0.001
            adjusted_probability['1'] -= (bowler_skill - 50) * 0.001
            adjusted_probability['2'] -= (bowler_skill - 50) * 0.001
            adjusted_probability['3'] -= (bowler_skill - 50) * 0.001
            adjusted_probability['4'] -= (bowler_skill - 50) * 0.001
            adjusted_probability['6'] -= (bowler_skill - 50) * 0.001
            adjusted_probability['W'] += (bowler_skill - 50) * 0.001

            total_prob = sum(adjusted_probability.values())
            for key in adjusted_probability:
                adjusted_probability[key] /= total_prob

            return adjusted_probability
    except Exception as e:
        print(f"Error: {e}")
        return None, e


def calc_dynamic_field_probability(fielder_skill):
    base_prob = {'Caught': 0.8, 'Dropped': 0.2}

    adjusted_prob = base_prob.copy()
    adjusted_prob['Caught'] += (fielder_skill - 60) * 0.001
    adjusted_prob['Dropped'] -= (fielder_skill - 60) * 0.001

    # Normalize the adjusted probabilities to ensure they add up to 1
    total_prob = sum(adjusted_prob.values())
    for key in adjusted_prob:
        adjusted_prob[key] /= total_prob

    return adjusted_prob

def calc_dynamic_runout(fielder_skill):
    base_prob = {'Direct Hit': 0.1, 'Missed': 0.9}
    adjusted_prob = base_prob.copy()
    adjusted_prob['Direct Hit'] += (fielder_skill - 55) * 0.001
    adjusted_prob['Missed'] -= (fielder_skill - 55) * 0.001

    # Ensure probabilities are within the range [0.03, 1]
    for key in adjusted_prob:
        adjusted_prob[key] = max(0.03, min(1, adjusted_prob[key]))

    # Normalize the adjusted probabilities to ensure they add up to 1
    total_prob = sum(adjusted_prob.values())
    for key in adjusted_prob:
        adjusted_prob[key] /= total_prob

    return adjusted_prob