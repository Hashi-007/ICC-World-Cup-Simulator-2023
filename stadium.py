import csv
from Pitch import Pitch, PitchType
import random
class Stadium:
    def __init__(self, name, location):
        self.name = name
        self.city = location
        self.pitch_type = self.assignPitch()

    def assignPitch(self):
        return Pitch(random.choice(list(PitchType)))




with open('data/csv_files/Stadiums.csv', 'r') as file:
    reader = csv.DictReader(file)
    stadiums = []
    for row in reader:
        name = row['Name']
        city = row['City']
        stadium = Stadium(name, city)
        stadiums.append(stadium)




