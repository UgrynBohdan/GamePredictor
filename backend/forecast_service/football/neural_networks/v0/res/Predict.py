import torch
import json
import joblib
import os
from loguru import logger

from .models.model import MyModel
from .RequestToDataset import RequestToDataset
from .DataEncoding import DataEncoding


class Predict:
    """
        Клас для ініціалізації моделі та виконання прогнозів.
        Завантажує необхідні трансформатори та стан моделі.
    """
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f'Доступний пристрій: {self.device}')
        self._file_path = os.path.dirname(os.path.abspath(__file__))

        if self.device == 'cpu':
            self.model_state_dict = self.predict_log(torch.load, 'Завантаження даних моделі.', self._file_path + '/models/model_state_dict_epoch_11.pt', weights_only=False, map_location=torch.device('cpu'))
        else:
            self.model_state_dict = self.predict_log(torch.load, 'Завантаження даних моделі.', self._file_path + '/models/model_state_dict_epoch_11.pt', weights_only=False)
        
        try:
            self.model = MyModel(len(self.model_state_dict['X_columns']), len(self.model_state_dict['y_columns'])).to(self.device)
            self.model.load_state_dict(self.model_state_dict['state_model'])
            self.model.eval()
            logger.info('Модель створено.')
        except Exception as e:
            logger.error(f'Помилка створення моделі!\n{e}')
            raise

        try:
            self.requestToDataset = RequestToDataset()
            self.dataEncoding = DataEncoding()
            logger.info('Трансформатори створено.')
        except Exception as e:
            logger.error(f'Помилка створення трансформаторів!\n{e}')
            raise

        self.scaler_y = self.predict_log(joblib.load, 'Завантаження scaler_y', self._file_path + '/transformers/scaler_y.joblib')


    def predict_log(self, f, message: str, *args, **kwargs):
        try:
            res = f(*args, **kwargs)
            logger.info(message)
            return res
        except Exception as e:
            logger.error(f'Помилка! {message} - {e}')
            raise


    def predict(self, X: dict):
        '''
            Приймає запит користувача, повертає відповідь моделі
        '''
        try:
            X = self.requestToDataset.request_to_ds(X)
            X = self.dataEncoding.encode(X)
            logger.info('Запит трансформовано.')
        except Exception as e:
            logger.error(f'Помилка трансформації запиту!\n{e}')
            raise
        
        pred = self.predict_log(self.model, 'Прогноз отримано.', torch.tensor(X.values, dtype=torch.float32).to(self.device))

        y = self.predict_log(self.scaler_y.inverse_transform, 'Відповідь розкодовано.', pred.cpu().detach().numpy())
        
        return y


if __name__ == '__main__':
    with open('./example/example.json', 'r', encoding='utf-8') as f:
        example = json.load(f)
    
    predict = Predict()
    res = predict.predict(example)
    print('\n\n\n')
    print(res)
    print(f"Приблизні результати команди №1 {example['home_club_name']}: {res[0][0]}")
    print(f"Приблизні результати команди №2 {example['away_club_name']}: {res[0][1]}")