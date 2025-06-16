from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
import hashlib
import os
import json
from loguru import logger
from config import *
import logger_config

from football.neural_networks.v0 import Predict

# FIXME Завжди будуйте абсолютні шляхи до файлів, використовуючи os.path.join замість os.chdir(os.path.dirname(os.path.abspath(__file__)))

class ForecastService:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        self._loading_json()
        
        try:
            self.predict_model = Predict()
            self._redis_connect()
        except Exception as e:
            logger.critical(f"Критична помилка при ініціалізації ForecastService: {e}")
            raise
        
        self._setup_routes()


    def _redis_connect(self):
        try:
            # Налаштування кешу
            self.app.config['CACHE_TYPE'] = CACHE_TYPE
            self.app.config['CACHE_REDIS_HOST'] = CACHE_REDIS_HOST
            self.app.config['CACHE_REDIS_PORT'] = CACHE_REDIS_PORT
            self.app.config['CACHE_REDIS_DB'] = CACHE_REDIS_DB
            self.app.config['CACHE_REDIS_URL'] = CACHE_REDIS_URL
            self.app.config['CACHE_DEFAULT_TIMEOUT'] = CACHE_DEFAULT_TIMEOUT # Стандартний TTL в секундах

            self.cache = Cache(self.app)
        except Exception as e:
            logger.critical(f"Критична помилка при підключенні до Redis: {e}")
            raise


    def _loading_json(self):
        # Змінити робочу директорію на директорію, де лежить цей файл
        # os.chdir(os.path.dirname(os.path.abspath(__file__)))
        source = os.path.dirname(os.path.abspath(__file__)) + '/football/data/for_frontend'
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
            logger.error(f'Критична помилка при завантаженні JSON-файлів: {e}')
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

    
    def _make_json_cache_key(*args, **kwargs):
        """
        Створює унікальний кеш-ключ для POST-запитів на основі JSON-тіла.
        Ця функція є статичним методом або окремою функцією,
        оскільки декоратор cache.cached вимагає, щоб вона не була методом екземпляра.
        """
        # request - це глобальний об'єкт Flask, доступний у контексті запиту
        json_data = request.get_json(silent=True) # silent=True щоб не викликати помилку, якщо JSON недійсний
        
        if json_data is None:
            # Якщо JSON-тіло відсутнє або недійсне, використовуємо просту комбінацію URL + query string
            logger.warning("JSON-тіло запиту відсутнє або недійсне для кешування.")
            return request.path + request.query_string.decode('utf-8')

        try:
            sorted_json_str = json.dumps(json_data, sort_keys=True, ensure_ascii=False)
            return hashlib.md5(sorted_json_str.encode('utf-8')).hexdigest()
        except TypeError as e:
            logger.warning(f"Не вдалося серіалізувати JSON-дані для кешування (TypeError): {e}. Використовую URL.")
            return request.path + request.query_string.decode('utf-8')
        except Exception as e:
            logger.error(f"Неочікувана помилка при генерації кеш-ключа з JSON-тіла: {e}. Використовую URL.")
            return request.path + request.query_string.decode('utf-8')


    def _setup_routes(self):
        @self.app.route('/predict', methods=['POST'])
        @self.cache.cached(timeout=30, make_cache_key=self._make_json_cache_key) # Оновлений декоратор кешування: make_cache_key використовує JSON-тіло
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
        self.app.run(host='0.0.0.0', port=port, debug=debug)



if __name__ == '__main__':
    server = ForecastService()
    server.run(debug=False)
