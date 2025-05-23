from flask import Flask
import joblib

app = Flask(__name__)
model = joblib.load('../../model/res/random_forest_model.pkl')

@app.route('/predict')
def home():
    # Доробити використання моделі, Хоча знаєш, краще створи в папці model/res створи папку з random_forest_models і в ній створи папку v0 і в неї запхай файл моделі і створи файл .py з функцією де ця модель використовує всі перетворення даних з json і повертає результат
    return "Сервер працює!"

if __name__ == '__main__':
    app.run(port=5001, debug=True)