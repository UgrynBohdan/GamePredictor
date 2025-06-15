import os
# Змінити робочу директорію на директорію, де лежить цей файл
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import json
import pandas as pd
import joblib
from loguru import logger
from pathlib import Path

class RequestToDataset:
    def __init__(self):
        project_root = Path(__file__).resolve().parents[3] # Переконайтеся, що [4] відповідає вашій структурі

        logger.info(f"Коренева директорія проєкту: {project_root}")

        try:
            self.competitions = pd.read_csv(project_root / 'data' / 'raw' / 'competitions.csv')
            self.games = pd.read_csv(project_root / 'data' / 'raw' / 'games.csv')
            self.clubs = pd.read_csv(project_root / 'data' / 'processed' / 'clubs_mod.csv')

            self.X = joblib.load('./transformers/X_columns.joblib')
            self.formation_code_map = joblib.load('./transformers/formation_code_map.joblib')

            logger.info("Дані DF та моделі завантажено успішно.")
        except Exception as e:
            logger.critical(f"Критична помилка завантаження даних DF для моделі: {e}")
            raise


    def request_to_ds_log(self, f, message: str, *args, **kwargs):
        try:
            res = f(*args, **kwargs)
            logger.info(message)
            return res
        except Exception as e:
            logger.error(f'Помилка! {message} - {e}')
            raise


    def request_to_ds(self, request: dict) -> pd.DataFrame:
        '''
            Функція для перетворення запиту користувача на DataFrame для моделі
        '''
        df = pd.DataFrame()
        df[self.X] = None
        df['competition_id'] = [0]

        df = self.request_to_ds_log(self.add_competition_id, "Додано competition_id.", df, request)

        df = self.request_to_ds_log(self.add_season, "Додано season.", df, request)

        df = self.request_to_ds_log(self.add_round, "Додано round.", df)

        df = self.request_to_ds_log(self.add_clubs_id, "Додано clubs_id.", df, request)

        df = self.request_to_ds_log(self.add_clubs_position, "Додано clubs_position.", df)

        df = self.request_to_ds_log(self.add_clubs_manager_name, "Додано clubs_manager_name.", df)

        df = self.request_to_ds_log(self.add_attendance, "Додано attendance.", df, request)

        df = self.request_to_ds_log(self.add_referee, "Додано referee.", df, request)

        df = self.request_to_ds_log(self.add_competition_data, "Додано competition_data.", df, request)

        home_columns = [
            'squad_size_home',
            'average_age_home', 'foreigners_number_home',
            'foreigners_percentage_home', 'national_team_players_home',
            'stadium_seats_home', 'last_season_home', 'total_market_value_home',
            'total_market_value_max_home', 'total_is_win_home',
        ]

        df = self.request_to_ds_log(self.add_club_data, "Додано home_club_data.", df, 'home_club_id', home_columns)

        away_columns = [
            'squad_size_away',
            'average_age_away', 'foreigners_number_away',
            'foreigners_percentage_away', 'national_team_players_away',
            'stadium_seats_away', 'last_season_away', 'total_market_value_away',
            'total_market_value_max_away', 'total_is_win_away',
        ]

        df = self.request_to_ds_log(self.add_club_data, "Додано away_club_data.", df, 'away_club_id', away_columns)

        df = self.request_to_ds_log(self.add_date, "Додано дату.", df, request)

        df = self.request_to_ds_log(self.add_clubs_formation, "Додано clubs_formation.", df, request)

        df = self.request_to_ds_log(self.add_clubs_net_transfer_record, "Додано clubs_net_transfer_record.", df)

        df = self.request_to_ds_log(self.add_stadium, "Додано stadium.", df, request)

        df = self.request_to_ds_log(self.add_clubs_stadium_name, "Додано clubs_stadium_name.", df)
        
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
        df[['name', 'sub_type', 'type', 'country_id', 'is_major_national_league']] = self.competitions[self.competitions['competition_id'] == df['competition_id'].iloc[0]][['name', 'sub_type', 'type', 'country_id', 'is_major_national_league']].iloc[0]
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
    res.to_csv('./example/formulated_request.csv', index=False)
    print('\n\n\n\n')
    print(res)
    print(res.columns[res.isnull().all()])
    print(res.isnull().all().all())
    
