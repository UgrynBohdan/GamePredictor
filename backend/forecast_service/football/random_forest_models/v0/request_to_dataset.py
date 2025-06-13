import os
# Змінити робочу директорію на директорію, де лежить цей файл
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import json
import pandas as pd

def request_to_ds(request):
    '''
        Функція для перетворення запиту користувача на DataFrame для моделі
    '''
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    X = [
        #'game_id',
        'competition_id', # За competition_code можна визначити, може задати користувач # є (competition_code)
        'season', # це рік, може задати користувач # є (data)
        'round', # хз
        'date', # дата, може задати користувач
        'home_club_id', # може задати користувач # є (home_club_name)
        'away_club_id', # може задати користувач # є (away_club_id)
        #  'home_club_goals',
        #  'away_club_goals',
        'home_club_position', # хз
        'away_club_position', # хз
        'home_club_manager_name', # хз
        'away_club_manager_name', # хз
        'stadium', # може задати користувач
        'attendance', # може задати користувач
        'referee', # може задати користувач
        'home_club_formation', # може задати користувач (з наприклад https://ua.tribuna.com/uk/football/match)
        'away_club_formation', # може задати користувач (з наприклад https://ua.tribuna.com/uk/football/match)
        #  'competition_type',
        'domestic_competition_id_home_club', # дістається з home_club_id
        'squad_size_home_club', # дістається з home_club_id
        'average_age_home_club', # дістається з home_club_id
        'foreigners_number_home_club', # дістається з home_club_id
        'national_team_players_home_club', # дістається з home_club_id
        'stadium_name_home_club', # дістається з home_club_id
        'stadium_seats_home_club', # дістається з home_club_id
        'net_transfer_record_home_club', # дістається з home_club_id
        'last_season_home_club', # дістається з home_club_id
        'domestic_competition_id_away_club', # дістається з away_club_id
        'squad_size_away_club', # дістається з away_club_id
        'average_age_away_club', # дістається з away_club_id
        'foreigners_number_away_club', # дістається з away_club_id
        'national_team_players_away_club', # дістається з away_club_id
        'stadium_name_away_club', # дістається з away_club_id
        'stadium_seats_away_club', # дістається з away_club_id
        'net_transfer_record_away_club', # дістається з away_club_id
        'last_season_away_club', # дістається з away_club_id
        'country_id', # дістається з competition_id
        #  'confederation',
        'is_major_national_league' # дістається з competition_id
    ]

    df = pd.DataFrame()
    df[X] = None
    df['competition_id'] = [0]

    # Завантаження потрібних сирих даних
    games = pd.read_csv('../../data/raw/games.csv')
    clubs = pd.read_csv('../../data/raw/clubs.csv')
    competitions = pd.read_csv('../../data/raw/competitions.csv')
    
    # Заповнення df
    # competition_id
    df['competition_id'] = competitions[competitions['competition_code'] == request['competition_code']]['competition_id'].values[0]

    # season, date
    df['season'] = pd.to_datetime(request['date']).year
    df['date'] = request['date']

    # round
    # найпоширеніший код
    df['round'] = games['round'].mode()[0]

    # home_club_id, away_club_id
    df['home_club_id'] = clubs[clubs['name'] == request['home_club_name']]['club_id'].values
    df['away_club_id'] = clubs[clubs['name'] == request['away_club_name']]['club_id'].values

    # home_club_position, away_club_position
    df['home_club_position'] = games['home_club_position'].mode()[0]
    df['away_club_position'] = games['away_club_position'].mode()[0]
    
    # home_club_manager_name, away_club_manager_name
    df['home_club_manager_name'] = games['home_club_manager_name'].mode()[0]
    df['away_club_manager_name'] = games['away_club_manager_name'].mode()[0]

    # stadium
    df['stadium'] = request['stadium']

    # attendance
    df['attendance'] = request['attendance']

    # referee
    df['referee'] = request['referee']

    # domestic_competition_id_home_club,  
    # squad_size_home_club,  
    # average_age_home_club,  
    # foreigners_number_home_club,  
    # national_team_players_home_club,  
    # stadium_name_home_club,  
    # stadium_seats_home_club,  
    # last_season_home_club
    df[[
        'domestic_competition_id_home_club', 'squad_size_home_club',
        'average_age_home_club', 'foreigners_number_home_club',
        'national_team_players_home_club', 'stadium_name_home_club',
        'stadium_seats_home_club', 'last_season_home_club', 'net_transfer_record_home_club'
    ]] = clubs[clubs['club_id'] == df['home_club_id'].values[0]][[
        'domestic_competition_id', 'squad_size',
        'average_age', 'foreigners_number',
        'national_team_players', 'stadium_name',
        'stadium_seats', 'last_season', 'net_transfer_record'
    ]].values

    # domestic_competition_id_away_club,  
    # squad_size_away_club,  
    # average_age_away_club,  
    # foreigners_number_away_club,  
    # national_team_players_away_club,  
    # stadium_name_away_club,  
    # stadium_seats_away_club,  
    # last_season_away_club
    df[[
        'domestic_competition_id_away_club', 'squad_size_away_club',
        'average_age_away_club', 'foreigners_number_away_club',
        'national_team_players_away_club', 'stadium_name_away_club',
        'stadium_seats_away_club', 'last_season_away_club', 'net_transfer_record_away_club'
    ]] = clubs[clubs['club_id'] == df['away_club_id'].values[0]][[
        'domestic_competition_id', 'squad_size',
        'average_age', 'foreigners_number',
        'national_team_players', 'stadium_name',
        'stadium_seats', 'last_season', 'net_transfer_record'
    ]].values

    # country_id, is_major_national_league
    df[['country_id', 'is_major_national_league']] = competitions[competitions['competition_id'] == df['competition_id'].values[0]][['country_id', 'is_major_national_league']].values


    # home_club_formation_code, away_club_formation_code
    df['home_club_formation'] = request['home_club_formation']
    df['away_club_formation'] = request['away_club_formation']

    # df['away_club_formation'] = None
    return df




if __name__ == "__main__":
    with open('./example.json', 'r', encoding='utf-8') as f:
        example = json.load(f)
    
    res = request_to_ds(example)
    print(res)
    print(res.columns[res.isnull().all()])
    
