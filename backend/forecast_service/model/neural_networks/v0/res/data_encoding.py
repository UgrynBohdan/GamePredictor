# Тестую кодування даних, для подальшого перетворення даних користувача
import os
# Змінити робочу директорію на директорію, де лежить цей файл
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import joblib
import numpy
from loguru import logger

# factorize_maps = joblib.load('../res/transformers/label_encoding_maps.joblib')
class DataEncoding:
    def __init__(self):
        self.factorize_maps = joblib.load('../res/transformers/label_encoding_maps.joblib')

        self.stadium_code_map = joblib.load('./transformers/stadium_code_map.joblib')

        self.scaler = joblib.load('./transformers/scaler.joblib')

    def encode(self, df):
        """
            Закодовує стовпці в зрозумілий вигляд для моделі
        """
        # os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # stadium_code_map = joblib.load('./transformers/stadium_code_map.joblib')

        df = self.encode_stadium(df)
        # df['stadium_code'] = df['stadium_code'].astype(str).map(stadium_code_map)

        df = self.encode_clubs_stadium_name(df)
        # df['stadium_name_home_code'] = df['stadium_name_home_code'].astype(str).map(stadium_code_map)
        # df['stadium_name_away_code'] = df['stadium_name_away_code'].astype(str).map(stadium_code_map)

        df = self.encode_categorical_features(df)
        # for col in [c for c in df.columns if df[c].dtype == numpy.dtype('O')]:
        #     df[col] = df[col].apply(lambda x: factorize_value(col, x))

        # scaler = joblib.load('./transformers/scaler.joblib')

        cols_for_norm = df.drop('is_major_national_league', axis=1).columns
        df = self.normalize(df, cols_for_norm)
        # df[cols_for_norm] = scaler.transform(df[cols_for_norm])

        df = self.encode_is_major_national_league(df)
        # df['is_major_national_league'] = df['is_major_national_league'].astype(float)

        return df

    def encode_stadium(self, df):
        df['stadium_code'] = df['stadium_code'].astype(str).map(self.stadium_code_map)
        return df

    def encode_clubs_stadium_name(self, df):
        df['stadium_name_home_code'] = df['stadium_name_home_code'].astype(str).map(self.stadium_code_map)
        df['stadium_name_away_code'] = df['stadium_name_away_code'].astype(str).map(self.stadium_code_map)
        return df
    
    # @logger.catch()
    def encode_categorical_features(self, df):
        def factorize_value(col, value):
            try:
                return self.factorize_maps[col].index(value)
            except ValueError:
                return -1
        
        for col in [c for c in df.columns if df[c].dtype == numpy.dtype('O')]:
            df[col] = df[col].apply(lambda x: factorize_value(col, x))
        return df
    
    def normalize(self, df, cols_for_norm):
        df[cols_for_norm] = self.scaler.transform(df[cols_for_norm])
        return df
    
    def encode_is_major_national_league(self, df):
        df['is_major_national_league'] = df['is_major_national_league'].astype(float)
        return df
    

if __name__ == '__main__':
    df = pd.read_csv('./example/formulated_request.csv')
    encoder = DataEncoding()
    df = encoder.encode(df)
    # df.to_csv('./example/encoded.csv', index=False)
    print(df)
    print(df.dtypes)