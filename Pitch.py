from enum import Enum

class PitchType(Enum):
    BATTING = 'Batting Pitch'
    BOWLING = 'Bowling Pitch'
    NEUTRAL = 'Neutral Pitch'

class Pitch:
    def __init__(self, pitch_type):
        self.pitch_type = pitch_type
        self.base_probabilities = self.getBaseProbabilities()

    def getBaseProbabilities(self):
        if self.pitch_type == PitchType.NEUTRAL:
            return {
                    'dot': 0.50,  # Probability of a dot ball
                    '1': 0.23,  # Probability of scoring 1 run
                    '2': 0.11,  # Probability of scoring 2 runs
                    '3': 0.02,  # Probability of scoring 3 runs
                    '4': 0.06,  # Probability of hitting a boundary (4 runs)
                    '6': 0.025,  # Probability of hitting a six (6 runs)
                    'W': 0.045,  # Probability of getting out
                    'extra': 0.01  # Probability of an extra run (wide or no-ball)
                }
        elif self.pitch_type == PitchType.BATTING:
            return {
                    'dot': 0.43,  # Probability of a dot ball
                    '1': 0.23,  # Probability of scoring 1 run
                    '2': 0.14,  # Probability of scoring 2 runs
                    '3': 0.04,  # Probability of scoring 3 runs
                    '4': 0.07,  # Probability of hitting a boundary (4 runs)
                    '6': 0.04,  # Probability of hitting a six (6 runs)
                    'W': 0.04,  # Probability of getting out
                    'extra': 0.01  # Probability of an extra run (wide or no-ball)
                }
        elif self.pitch_type == PitchType.BOWLING:
            return {
                    'dot': 0.6,  # Probability of a dot ball
                    '1': 0.2,  # Probability of scoring 1 run
                    '2': 0.09,  # Probability of scoring 2 runs
                    '3': 0.02,  # Probability of scoring 3 runs
                    '4': 0.02,  # Probability of hitting a boundary (4 runs)
                    '6': 0.01,  # Probability of hitting a six (6 runs)
                    'W': 0.05,  # Probability of getting out
                    'extra': 0.01  # Probability of an extra run (wide or no-ball)
                }