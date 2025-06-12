from flask import Flask, request, jsonify
from flask_cors import CORS
from loguru import logger

from model.neural_networks.v0.res.Predict import Predict


class ForecastService:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.predict = Predict()
        self.setup_routes()

    def forecast_service_log(self, f, message: str, *args, **kwargs):
        try:
            res = f(*args, **kwargs)
            logger.info(message)
            return res
        except Exception as e:
            logger.error(f'Помилка! {message}\n{e}')
            raise

    def setup_routes(self):
        @self.app.route('/predict', methods=['POST'])
        def predict():
            data = self.forecast_service_log(request.get_json, "Запит отримано.")

            res = self.forecast_service_log(self.predict.predict, "Передбачення отримано.", data).tolist()[0]
            
            return jsonify({'predict': res})
        

    def run(self, port=5001, debug=True):
        self.app.run(port=port, debug=debug)


if __name__ == '__main__':
    server = ForecastService()
    server.run()