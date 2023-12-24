import csv
from players import Player, Batting_Position
from team import Team

def extraction_of_data(csv_file_path):
    # List that will store player objects
    players = []

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)

        # Iterate Through each row
        for row in reader:

            name = row['Name']
            role = row['Role']
            batting_skill = int(row['Batting Skill'])
            batting_type_main = row['Batting Type Main']
            batting_type_sub = int(row['Batting Type Sub']) if row.get('Batting Type Sub') else None
            bowling_skill = int(row['Bowling Skill']) if row.get('Bowling Skill') else 30
            bowling_type = row.get('Bowling Type', None)
            fielding_skill = int(row['Fielding Skill'])

            batting_position = Batting_Position(batting_type_main, batting_type_sub)

            player = Player(name, role, batting_skill, batting_position, bowling_skill, bowling_type, fielding_skill)

            players.append(player)

        team_name = csv_file_path.split('/')[-1].split('.')[0]

        team = Team(team_name)

        for player in players:
            team.add_player(player)

        return team



team_pakistan = extraction_of_data('data/csv_files/Pakistan.csv')
team_india = extraction_of_data('data/csv_files/India.csv')
team_sri_lanka = extraction_of_data('data/csv_files/Sri Lanka.csv')
team_australia = extraction_of_data('data/csv_files/Australia.csv')
team_south_africa = extraction_of_data('data/csv_files/South Africa.csv')
team_afghanistan = extraction_of_data('data/csv_files/Afghanistan.csv')
team_england = extraction_of_data('data/csv_files/England.csv')
team_netherlands = extraction_of_data('data/csv_files/Netherlands.csv')
team_bangladesh = extraction_of_data('data/csv_files/Bangladesh.csv')
team_new_zealand = extraction_of_data('data/csv_files/New Zealand.csv')

teams = []
teams.append(team_bangladesh)
teams.append(team_netherlands)
teams.append(team_afghanistan)
teams.append(team_england)
teams.append(team_pakistan)
teams.append(team_south_africa)
teams.append(team_new_zealand)
teams.append(team_india)
teams.append(team_australia)
teams.append(team_sri_lanka)