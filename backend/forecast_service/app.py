import os
# Змінити робочу директорію на директорію, де лежить цей файл
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, request, jsonify
import json
from model.res.random_forest_models.v0.run import predict as model_pr
from loguru import logger
# logger.add("app.log", rotation="10 MB")
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    logger.warning("Спроба отримати запит:")
    try:
        data = request.get_json()
        logger.info(f'Запит отримано!\n{data}')
    except Exception as e:
        logger.error(f"Помилка при отриманні JSON запиту: {e}")
        return jsonify({"error": "Invalid JSON"}), 400



    logger.warning('Спроба отримати прогноз:')
    try:
        res = model_pr(data)
        logger.info(f'Прогноз отримано!\n{res}')
    except Exception as e:
        logger.error(f"Помилка при отриманні прогнозу: {e}")
        return jsonify({"error": "Prediction failed"}), 500



    logger.warning('Спроба перевести результати в json:')
    try:
        res = res.tolist()[0]
        logger.info('Переведено успішно!')
    except Exception as e:
        logger.error(f"Помилка при конвертації результатів: {e}")
        return jsonify({"error": "Result conversion failed"}), 500

    logger.warning('Повернення результатів')
    return jsonify(res)


@app.route('/all_fields', methods=['GET'])
def all_fields():
    source = './model/res/random_forest_models/v0/for_frontend'

    try:
        with open(source + '/clubs_name.json', 'r', encoding='utf-8') as f1:
            clubs_name = json.load(f1)
        with open(source + '/referee.json', 'r', encoding='utf-8') as f2:
            referees = json.load(f2)
        with open(source + '/stadiums.json', 'r', encoding='utf-8') as f3:
            stadiums = json.load(f3)

        res = {
            "clubs_name": clubs_name,
            "referees": referees,
            "stadiums": stadiums
        }

        return jsonify(res)
    
    except Exception as e:
        logger.error(f'Помилка при завантаженні JSON: {e}')
        return jsonify({"error": "Failed to load JSON files"}), 500



if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logger.info("Запуск!")
    app.run(port=5001, debug=True)