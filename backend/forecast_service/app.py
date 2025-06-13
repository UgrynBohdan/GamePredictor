from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from loguru import logger

from football.neural_networks.v0 import Predict


class ForecastService:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.predict_model = Predict()
        self.setup_routes()
        self._loading_json()


    def _loading_json(self):
        # Змінити робочу директорію на директорію, де лежить цей файл
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        source = './football/data/for_frontend'
        try:
            # Завантаження JSON-файлів
            with open(source + '/clubs_name.json', 'r', encoding='utf-8') as f1:
                clubs_name = json.load(f1)
            with open(source + '/referees.json', 'r', encoding='utf-8') as f2:
                referees = json.load(f2)
            with open(source + '/stadiums.json', 'r', encoding='utf-8') as f3:
                stadiums = json.load(f3)
            with open(source + '/competitions_code.json', 'r', encoding='utf-8') as f3:
                competitions_code = json.load(f3)

            self.res = {
                "clubs_name": clubs_name,
                "referees": referees,
                "stadiums": stadiums,
                "competitions_code": competitions_code
            }
            logger.info('Успішно завантажено JSON-файли.')
        except Exception as e:
            logger.critical(f'Критична помилка при завантаженні JSON-файлів: {e}')
            self.res = {"error": "Failed to load initial JSON files"}


    def _execute_and_log_error(self, func, success_message: str, *args, **kwargs):
        """
        Допоміжна функція для виконання іншої функції, логування її успіху/невдачі
        та повторного викликання винятків.
        """
        try:
            res = func(*args, **kwargs)
            logger.info(success_message)
            return res
        except Exception as e:
            logger.error(f'Помилка при виконанні операції: "{success_message}": {e}')
            raise


    def setup_routes(self):
        @self.app.route('/predict', methods=['POST'])
        def predict_route():
            try:
                data = self._execute_and_log_error(
                    request.get_json,
                    "Запит отримано та JSON успішно розпарсено."
                )

                final_prediction = self._execute_and_log_error(
                    self.predict_model.predict,
                    "Передбачення отримано",
                    data
                ).tolist()[0]
                
                return jsonify({'predict': final_prediction})

            except Exception as e:
                logger.error(f"Помилка при обробці запиту /predict: {e}")
                return jsonify({'message': f'Error! Сталася внутрішня помилка сервера!!!'}), 500


        @self.app.route('/all_fields', methods=['GET'])
        def all_fields():
            # Перевіряємо, чи були дані успішно завантажені
            if "error" in self.res:
                logger.warning(f"Запит до /all_fields, але JSON-файли не були завантажені: {self.res['error']}")
                return jsonify({'message': self.res['error']}), 500
            return jsonify(self.res)


    def run(self, port=5001, debug=True):
        self.app.run(port=port, debug=debug)



if __name__ == '__main__':
    server = ForecastService()
    server.run()
