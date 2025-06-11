import os
# Змінити робочу директорію на директорію, де лежить цей файл
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import torch
import json
import joblib

from models.model import MyModel
from request_to_dataset import RequestToDataset
from data_encoding import DataEncoding

class Run:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.model_state_dict = torch.load('./models/model_state_dict_epoch_11.pt', weights_only=False)

        self.model = MyModel(len(self.model_state_dict['X_columns']), len(self.model_state_dict['y_columns'])).to(self.device)
        self.model.load_state_dict(self.model_state_dict['state_model'])
        self.model.eval()

        self.requestToDataset = RequestToDataset()
        self.dataEncoding = DataEncoding()

        self.scaler = joblib.load('./transformers/scaler_y.joblib')

    def predict(self, X):
        '''
            Приймає запит користувача, повертає відповідь моделі
        ''' 

        X = self.requestToDataset.request_to_ds(X)
        X = self.dataEncoding.encode(X)

        pred = self.model(torch.tensor(X.values, dtype=torch.float32).to(self.device))

        y = self.scaler.inverse_transform(pred.cpu().detach().numpy())
        
        return y


if __name__ == '__main__':
    with open('./example/example.json', 'r', encoding='utf-8') as f:
        example = json.load(f)
    
    run = Run()
    res = run.predict(example)
    print('\n\n\n')
    print(res)
    print(f'Приблизні результати команди №1 {example['home_club_name']}: {res[0][0]}')
    print(f'Приблизні результати команди №2 {example['away_club_name']}: {res[0][1]}')

    res = run.predict(example)
    print('\n\n\n')
    print(res)
    print(f'Приблизні результати команди №1 {example['home_club_name']}: {res[0][0]}')
    print(f'Приблизні результати команди №2 {example['away_club_name']}: {res[0][1]}')