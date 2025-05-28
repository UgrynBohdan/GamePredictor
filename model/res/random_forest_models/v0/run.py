import joblib
import pandas as pd
import json
from data_encoding import encode
from request_to_dataset import request_to_ds
import os

# Змінити робочу директорію на директорію, де лежить цей файл
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def predict(X):
    '''
        Приймає запит користувача, повертає відповідь моделі
    '''
    X = request_to_ds(X)
    X = encode(X)

    X = X.drop([
        'date', 'home_club_formation', 'away_club_formation',
        'net_transfer_record_home_club', 'net_transfer_record_away_club'
    ], axis=1)

    model = joblib.load('./random_forest_model.pkl')

    y = model.predict(X)
    return y


if __name__ == '__main__':
    with open('./example.json', 'r', encoding='utf-8') as f:
        example = json.load(f)
    
    res = predict(example)
    print(res)
    print(f'Приблизні результати команди №1 {example['home_club_name']}: {res[0][0]}')
    print(f'Приблизні результати команди №2 {example['away_club_name']}: {res[0][1]}')