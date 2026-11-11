import requests

# Вывод всех пользователей через users = db_session.query(User).all()
response = requests.get(
    "http://127.0.0.1:5000/users",
)
print(response.status_code)
print(response.json())

# Добавление пользователя
response = requests.post(
    "http://127.0.0.1:5000/users",
    json={"username": "user_6", "password": "12345", "email": "12345@mail.ru"},
)
print(response.status_code)
print(response.json())

# Получение данных о пользователе
response = requests.get("http://127.0.0.1:5000/users/14")
print(response.status_code)
print(response.json())

# Изменение данных пользователя
response = requests.patch(
    "http://127.0.0.1:5000/users/3", json={"username": "new_name", "password": "1234"}
)
print(response.status_code)
print(response.json())

# Удаление пользователя
response = requests.delete("http://127.0.0.1:5000/users/3")
print(response.status_code)
print(response.json())

# Создание объявления
response = requests.post(
    "http://127.0.0.1:5000/postings",
    json={"heading": "Пост 1", "description": "Мой новый пост", "owner_id": 1},
)
print(response.status_code)
print(response.json())

# Получение данных объявления
response = requests.get("http://127.0.0.1:5000/postings/3")
print(response.status_code)
print(response.json())

# Изменение данных объявления
response = requests.patch(
    "http://127.0.0.1:5000/postings/3",
    json={"heading": "Пост 3", "description": "Мой новый пост 3", "owner_id": 13},
)
print(response.status_code)
print(response.json())

# Удаление объявления
response = requests.delete("http://127.0.0.1:5000/postings/3", json={"owner_id": 13})
print(response.status_code)
print(response.json())
