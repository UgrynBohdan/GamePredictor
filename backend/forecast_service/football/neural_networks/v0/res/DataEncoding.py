# Тестую кодування даних, для подальшого перетворення даних користувача
import os
# Змінити робочу директорію на директорію, де лежить цей файл
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import joblib
import numpy
from loguru import logger

class DataEncoding:
    def __init__(self):
        self.factorize_maps = self.encode_log(joblib.load, "Завантаження карти категорій.", '../res/transformers/label_encoding_maps.joblib')
        self.stadium_code_map = self.encode_log(joblib.load, "Завантаження карти стадіонів.", './transformers/stadium_code_map.joblib')

        self.scaler = self.encode_log(joblib.load, 'Завантаження scaler.', './transformers/scaler.joblib')


    def encode_log(self, f, message: str, *args):
        try:
            res = f(*args)
            logger.info(message)
            return res
        except Exception as e:
            logger.error(f'Помилка! {message} - {e}')
            raise


    def encode(self, df: pd.DataFrame) -> pd.DataFrame:
        """
            Закодовує стовпці в зрозумілий вигляд для моделі
        """
        df = self.encode_log(self.encode_stadium, "Кодування стадіону.", df)

        df = self.encode_log(self.encode_clubs_stadium_name, "Кодування стадіонів клубів.", df)

        df = self.encode_log(self.encode_categorical_features, "Кодування категоріальних ознак.", df)

        cols_for_norm = df.drop('is_major_national_league', axis=1).columns
        df = self.encode_log(self.normalize, "Нормалізація.", df, cols_for_norm)

        df = self.encode_log(self.encode_is_major_national_league, "Кодування важливості ліги.", df)

        return df


    def encode_stadium(self, df: pd.DataFrame) -> pd.DataFrame:
        df['stadium_code'] = df['stadium_code'].astype(str).map(self.stadium_code_map)
        return df


    def encode_clubs_stadium_name(self, df: pd.DataFrame) -> pd.DataFrame:
        # FIXME Краще закодовувати клуби окремо, двома викликами функції
        df['stadium_name_home_code'] = df['stadium_name_home_code'].astype(str).map(self.stadium_code_map)
        df['stadium_name_away_code'] = df['stadium_name_away_code'].astype(str).map(self.stadium_code_map)
        return df


    def encode_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        # FIXME Краще передавати список зовні
        def factorize_value(col, value):
            try:
                return self.factorize_maps[col].index(value)
            except ValueError:
                return -1
        
        for col in [c for c in df.columns if df[c].dtype == numpy.dtype('O')]:
            df[col] = df[col].apply(lambda x: factorize_value(col, x))
        return df
    

    def normalize(self, df: pd.DataFrame, cols_for_norm: list) -> pd.DataFrame:
        df[cols_for_norm] = self.scaler.transform(df[cols_for_norm])
        return df
    

    def encode_is_major_national_league(self, df: pd.DataFrame) -> pd.DataFrame:
        df['is_major_national_league'] = df['is_major_national_league'].astype(float)
        return df
    


if __name__ == '__main__':
    df = pd.read_csv('./example/formulated_request.csv')
    encoder = DataEncoding()
    df = encoder.encode(df)

    print(df)
    print(df.dtypes)