import redis

# Підключення до Redis
# За замовчуванням: host='localhost', port=6379, db=0
r = redis.Redis(host='localhost', port=6379, db=0)

# Перевірка підключення
try:
    r.ping()
    print("Успішно підключено до Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"Помилка підключення до Redis: {e}")

# Встановлення значення (SET key value)
r.set('mykey', 'Привіт, Redis!')
print(f"Значення 'mykey' встановлено.")

# Встановлення значення з часом життя (TTL) в секундах (SETEX key seconds value)
r.setex('temp_key', 60, 'Це тимчасове значення') # Зникне через 60 секунд
print(f"Значення 'temp_key' встановлено на 60 секунд.")

# Отримання значення (GET key)
value = r.get('mykey')
if value:
    print(f"Значення 'mykey': {value.decode('utf-8')}")
else:
    print(f"Ключ 'mykey' не знайдено.")

temp_value = r.get('temp_key')
if temp_value:
    print(f"Значення 'temp_key': {temp_value.decode('utf-8')}")
else:
    print(f"Ключ 'temp_key' не знайдено або термін дії закінчився.")