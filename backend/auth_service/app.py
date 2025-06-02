from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_mysqldb import MySQL
from config import *
from loguru import logger

app = Flask(__name__)
CORS(app)

# DB config
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_PORT'] = 3307  # вказуєш явно порт!
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB

mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    # logger.warning("Спроба отримати запит:")
    try:
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = generate_password_hash(data['password'])
        logger.info(f'Запит отримано!')
    except Exception as e:
        logger.error(f"Помилка при отриманні JSON запиту: {e}")
        return jsonify({"error": "Invalid JSON"}), 400


    cur = mysql.connection.cursor()
    logger.info("Підключення до БД успішне!")

    try:
        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, password))
        mysql.connection.commit()

        cur.execute("SELECT username FROM users WHERE email = %s", (email,))
        row = cur.fetchone()

        logger.info('Користувача створено успішно!')
        return jsonify({'message': 'Користувача створено успішно', 'username': row[0]}), 201
    except:
        logger.error('Користувач з таким email або іменем вже існує!')
        return jsonify({'error': 'Користувач з таким email або іменем вже існує'}), 409

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        logger.info(f'Запит отримано!')
    except Exception as e:
        logger.error(f"Помилка при отриманні JSON запиту: {e}")
        return jsonify({"error": "Invalid JSON"}), 400

    cur = mysql.connection.cursor()
    logger.info("Підключення до БД успішне!")

    cur.execute("SELECT password_hash, username FROM users WHERE email = %s", (email,))
    row = cur.fetchone()
    if row and check_password_hash(row[0], password):
        logger.info('Вхід успішний!')
        return jsonify({'message': 'Вхід успішний', 'username': row[1]}), 200
    else:
        logger.error('Неправильний логін або пароль!')
        return jsonify({'error': 'Неправильний логін або пароль'}), 401

if __name__ == '__main__':
    logger.info("Запуск!")
    app.run(port=5002, debug=True)
