import os
# Змінити робочу директорію на директорію, де лежить цей файл
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import json
import pandas as pd
import joblib

class RequestToDataset:
    def __init__(self):
        self.competitions = pd.read_csv('../../../data/raw/competitions.csv')
        self.games = pd.read_csv('../../../data/raw/games.csv')
        self.clubs = pd.read_csv('./transformers/clubs_mod.csv')

        self.X = joblib.load('./transformers/X_columns.joblib')

        self.formation_code_map = joblib.load('./transformers/formation_code_map.joblib')

    def request_to_ds(self, request):
        '''
            Функція для перетворення запиту користувача на DataFrame для моделі
        '''
        # os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # X = joblib.load('./transformers/X_columns.joblib')

        df = pd.DataFrame()
        df[self.X] = None
        df['competition_id'] = [0]

        # Формування датасету з запиту користувача
        # competitions = pd.read_csv('../../../data/raw/competitions.csv')
        # games = pd.read_csv('../../../data/raw/games.csv')
        # clubs = pd.read_csv('./transformers/clubs_mod.csv')

        df = self.add_competition_id(df, request)
        # df['competition_id'] = competitions[competitions['competition_code'] == request['competition_code']]['competition_id'].iloc[0]

        df = self.add_season(df, request)
        # df['season'] = pd.to_datetime(request['date']).year

        df = self.add_round(df)
        # df['round'] = games['round'].mode()[0]

        df = self.add_clubs_id(df, request)
        # df['home_club_id'] = clubs[clubs['name'] == request['home_club_name']]['club_id'].values
        # df['away_club_id'] = clubs[clubs['name'] == request['away_club_name']]['club_id'].values

        # df['home_club_position'] = games['home_club_position'].mode()[0]
        # df['away_club_position'] = games['away_club_position'].mode()[0]
        df = self.add_clubs_position(df)
        # df['home_club_position'] = 3
        # df['away_club_position'] = 3

        df = self.add_clubs_manager_name(df)
        # df['home_club_manager_name'] = games['home_club_manager_name'].mode()[0]
        # df['away_club_manager_name'] = games['away_club_manager_name'].mode()[0]

        # attendance
        df = self.add_attendance(df, request)
        # df['attendance'] = request['attendance']

        # referee
        df = self.add_referee(df, request)
        # df['referee'] = request['referee']

        df = self.add_competition_data(df, request)
        # df[['name', 'sub_type', 'type', 'country_id', 'is_major_national_league']] = competitions[competitions['competition_code'] == request['competition_code']][['name', 'sub_type', 'type', 'country_id', 'is_major_national_league']].iloc[0]

        home_columns = [
            'squad_size_home',
            'average_age_home', 'foreigners_number_home',
            'foreigners_percentage_home', 'national_team_players_home',
            'stadium_seats_home', 'last_season_home', 'total_market_value_home',
            'total_market_value_max_home', 'total_is_win_home',
        ]

        df = self.add_club_data(df, 'home_club_id', home_columns)
        # df[[
        #     'squad_size_home',
        #     'average_age_home', 'foreigners_number_home',
        #     'foreigners_percentage_home', 'national_team_players_home',
        #     'stadium_seats_home', 'last_season_home', 'total_market_value_home',
        #     'total_market_value_max_home', 'total_is_win_home',
        # ]] = clubs[clubs['club_id'] == df['home_club_id'].values[0]][[
        #     'squad_size',
        #     'average_age', 'foreigners_number', 'foreigners_percentage',
        #     'national_team_players', 'stadium_seats',
        #     'last_season',
        #     'total_market_value', 'total_market_value_max', 'total_is_win'
        # ]].values

        away_columns = [
            'squad_size_away',
            'average_age_away', 'foreigners_number_away',
            'foreigners_percentage_away', 'national_team_players_away',
            'stadium_seats_away', 'last_season_away', 'total_market_value_away',
            'total_market_value_max_away', 'total_is_win_away',
        ]

        df = self.add_club_data(df, 'away_club_id', away_columns)
        # df[[
        #     'squad_size_away',
        #     'average_age_away', 'foreigners_number_away',
        #     'foreigners_percentage_away', 'national_team_players_away',
        #     'stadium_seats_away', 'last_season_away', 'total_market_value_away',
        #     'total_market_value_max_away', 'total_is_win_away',
        # ]] = clubs[clubs['club_id'] == df['away_club_id'].values[0]][[
        #     'squad_size',
        #     'average_age', 'foreigners_number', 'foreigners_percentage',
        #     'national_team_players', 'stadium_seats',
        #     'last_season',
        #     'total_market_value', 'total_market_value_max', 'total_is_win'
        # ]].values

        df = self.add_date(df, request)
        # df['year'] = pd.to_datetime(request['date']).year
        # df['month'] = pd.to_datetime(request['date']).month
        # df['day'] = pd.to_datetime(request['date']).day
        # df['dayofweek'] = pd.to_datetime(request['date']).dayofweek

        # formation_code_map = joblib.load('./transformers/formation_code_map.joblib')

        df = self.add_clubs_formation(df, request)
        # df['home_club_formation_code'] = formation_code_map[request['home_club_formation']]
        # df['away_club_formation_code'] = formation_code_map[request['away_club_formation']]

        df = self.add_clubs_net_transfer_record(df)
        # df['net_transfer_record_home_num'] = clubs[clubs['club_id'] == df['home_club_id'].values[0]]['net_transfer_record'].apply(parse_transfer_value).iloc[0]
        # df['net_transfer_record_away_num'] = clubs[clubs['club_id'] == df['away_club_id'].values[0]]['net_transfer_record'].apply(parse_transfer_value).iloc[0]

        df = self.add_stadium(df, request)
        # df['stadium_code'] = request['stadium']

        df = self.add_clubs_stadium_name(df)
        # df['stadium_name_home_code'] = clubs[clubs['club_id'] == df['home_club_id'].values[0]]['stadium_name'].iloc[0]
        # df['stadium_name_away_code'] = clubs[clubs['club_id'] == df['away_club_id'].values[0]]['stadium_name'].iloc[0]
        
        return df
    
    def add_competition_id(self, df, request):
        df['competition_id'] = self.competitions[self.competitions['competition_code'] == request['competition_code']]['competition_id'].iloc[0]
        return df
    
    def add_season(self, df, request):
        df['season'] = pd.to_datetime(request['date']).year
        return df
    
    def add_round(self, df):
        df['round'] = self.games['round'].mode()[0]
        return df
    
    def add_clubs_id(self, df, request):
        df['home_club_id'] = self.clubs[self.clubs['name'] == request['home_club_name']]['club_id'].values
        df['away_club_id'] = self.clubs[self.clubs['name'] == request['away_club_name']]['club_id'].values
        return df
    
    def add_clubs_position(self, df):
        df['home_club_position'] = 3
        df['away_club_position'] = 3
        return df
    
    def add_clubs_manager_name(self, df):
        df['home_club_manager_name'] = self.games['home_club_manager_name'].mode()[0]
        df['away_club_manager_name'] = self.games['away_club_manager_name'].mode()[0]
        return df
    
    def add_attendance(self, df, request):
        df['attendance'] = request['attendance']
        return df
    
    def add_referee(self, df, request):
        df['referee'] = request['referee']
        return df
    
    def add_competition_data(self, df: pd.DataFrame, request):
        # FIXME В df і так присутній competition_id, не потрібно визначати його з request
        df[['name', 'sub_type', 'type', 'country_id', 'is_major_national_league']] = self.competitions[self.competitions['competition_code'] == request['competition_code']][['name', 'sub_type', 'type', 'country_id', 'is_major_national_league']].iloc[0]
        return df

    def add_club_data(self, df, target_col, columns):
        df[columns] = self.clubs[self.clubs['club_id'] == df[target_col].values[0]][[
            'squad_size',
            'average_age', 'foreigners_number', 'foreigners_percentage',
            'national_team_players', 'stadium_seats',
            'last_season',
            'total_market_value', 'total_market_value_max', 'total_is_win'
        ]].values
        return df
    
    def add_date(self, df, request):
        # FIXME По суті це повноцінне перетворення даних в закодований вигляд, а в тебе є інший файл для цього
        df['year'] = pd.to_datetime(request['date']).year
        df['month'] = pd.to_datetime(request['date']).month
        df['day'] = pd.to_datetime(request['date']).day
        df['dayofweek'] = pd.to_datetime(request['date']).dayofweek
        return df
    
    def add_clubs_formation(self, df, request):
        # FIXME По суті це повноцінне перетворення даних в закодований вигляд, а в тебе є інший файл для цього
        df['home_club_formation_code'] = self.formation_code_map[request['home_club_formation']]
        df['away_club_formation_code'] = self.formation_code_map[request['away_club_formation']]
        return df
    
    def add_clubs_net_transfer_record(self, df):
        def parse_transfer_value(value):
            if pd.isnull(value):
                return None
            value = value.replace('€', '').replace('+', '').replace(' ', '')
            sign = -1 if '-' in value else 1
            value = value.replace('-', '')
            if value.endswith('m'):
                num = float(value[:-1]) * 1_000_000
            elif value.endswith('k'):
                num = float(value[:-1]) * 1_000
            else:
                num = float(value)
            return sign * num

        df['net_transfer_record_home_num'] = self.clubs[self.clubs['club_id'] == df['home_club_id'].values[0]]['net_transfer_record'].apply(parse_transfer_value).iloc[0]
        df['net_transfer_record_away_num'] = self.clubs[self.clubs['club_id'] == df['away_club_id'].values[0]]['net_transfer_record'].apply(parse_transfer_value).iloc[0]
        return df
    
    def add_stadium(self, df, request):
        df['stadium_code'] = request['stadium']
        return df

    def add_clubs_stadium_name(self, df):
        df['stadium_name_home_code'] = self.clubs[self.clubs['club_id'] == df['home_club_id'].values[0]]['stadium_name'].iloc[0]
        df['stadium_name_away_code'] = self.clubs[self.clubs['club_id'] == df['away_club_id'].values[0]]['stadium_name'].iloc[0]
        return df



if __name__ == "__main__":
    with open('./example/example.json', 'r', encoding='utf-8') as f:
        example = json.load(f)
    
    requestToDataset = RequestToDataset()
    res = requestToDataset.request_to_ds(example)
    print('\n\n\n\n')
    print(res)
    print(res.columns[res.isnull().all()])
    print(res.isnull().all().all())
    
