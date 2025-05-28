# Тестую кодування даних, для подальшого перетворення даних користувача

import pandas as pd
import pickle
import os
import sys

    
def encode(df):
    """
        Закодовує стовпці в зрозумілий вигляд для моделі
    """
    # Змінити робочу директорію на директорію, де лежить цей файл
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 0
    # df = df.drop(['confederation', 'competition_type'], axis=1)

    # 1
    # Label Encoding (для ordinal/порядкових ознак):
    col_for_LE = [
        'competition_id', 'round', 'home_club_manager_name','away_club_manager_name', 'stadium', 'referee',
        'domestic_competition_id_home_club', 'stadium_name_home_club','domestic_competition_id_away_club',
        'stadium_name_away_club'
    ]

    # Завантажити mapping
    with open('./transformers/label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)

    # Для кодування нових даних:
    for col in col_for_LE:
        mapping = {v: k for k, v in label_encoders[col].items()}
        df[col] = df[col].map(mapping).fillna(-1).astype(int)  # -1 для невідомих категорій




    # 2
    # Обробка дати
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['dayofweek'] = df['date'].dt.dayofweek  # 0 - понеділок, 6 - неділя

    # 3
    # Завантажити mapping
    with open('./transformers/formation_encoder.pkl', 'rb') as f:
        value_to_code = pickle.load(f)

    # Кодувати нові дані
    df['home_club_formation_code'] = df['home_club_formation'].astype(str).map(value_to_code).fillna(-1).astype(int)
    df['away_club_formation_code'] = df['away_club_formation'].astype(str).map(value_to_code).fillna(-1).astype(int)

    # 4
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

    # Приклад для DataFrame:
    df['net_transfer_record_home_club_num'] = df['net_transfer_record_home_club'].apply(parse_transfer_value)
    df['net_transfer_record_away_club_num'] = df['net_transfer_record_away_club'].apply(parse_transfer_value)


    # 5
    import joblib

    # Завантажити scaler
    scaler = joblib.load('./transformers/minmax_scaler.pkl')

    corr_col = [
        'competition_id', 'season', 'round', 'home_club_id',
        'away_club_id',
        'home_club_position', 'away_club_position', 'home_club_manager_name',
        'away_club_manager_name', 'stadium', 'attendance', 'referee',
        'domestic_competition_id_home_club', 'squad_size_home_club',
        'average_age_home_club', 'foreigners_number_home_club',
        'national_team_players_home_club', 'stadium_name_home_club',
        'stadium_seats_home_club',
        'last_season_home_club', 'domestic_competition_id_away_club',
        'squad_size_away_club', 'average_age_away_club',
        'foreigners_number_away_club', 'national_team_players_away_club',
        'stadium_name_away_club', 'stadium_seats_away_club',
        'last_season_away_club', 'country_id',
        'year', 'month', 'day', 'dayofweek',
        'home_club_formation_code', 'away_club_formation_code',
        'net_transfer_record_home_club_num',
        'net_transfer_record_away_club_num'
    ]
    # Застосувати до нових даних
    df[corr_col] = scaler.transform(df[corr_col])

    return df

if __name__ == '__main__':
    # Змінити робочу директорію на директорію, де лежить цей файл
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    df = pd.read_csv('./test.csv')
    df = encode(df)
    print(df)