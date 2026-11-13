import requests


# # Добавление пользователя
# response = requests.post(
#     "http://127.0.0.1:5000/users",
#     json={"username": "user_3", "password": "12345", "email": "12345@mail.ru"},
# )
# print(response.status_code)
# print(response.json())

# # Получение данных о пользователе
# response = requests.get("http://127.0.0.1:5000/users/1")
# print(response.status_code)
# print(response.json())

# # Аавторизация пользователя
# s = requests.Session()
# response = s.post(
#     "http://127.0.0.1:5000/login",
#     json={"username": "new_name2", "password": "12345"},
# )
# print(response.status_code)
# print(response.json())

# # Изменение данных пользователя (username)
# response = s.patch(
#     "http://127.0.0.1:5000/users/1",
#     json={"username": "new_name2"}
# )
# print(response.status_code)
# print(response.json())
#
# # Изменение данных пользователя (password)
# response = s.patch(
#     "http://127.0.0.1:5000/users/1",
#     json={"password": "12345"}
# )
# print(response.status_code)
# print(response.json())
#
# # Изменение данных пользователя (email)
# response = s.patch(
#     "http://127.0.0.1:5000/users/1",
#     json={"email": "1234@mal.ru"}
# )
# print(response.status_code)
# print(response.json())

# # Удаление пользователя
# response = s.delete("http://127.0.0.1:5000/users/1")
# print(response.status_code)
# print(response.json())

# # # Создание объявления
# response = requests.post(
#     "http://127.0.0.1:5000/postings",
#     json={"heading": "Пост 1", "description": "Мой новый пост", "owner_id": 2},
# )
# print(response.status_code)
# print(response.json())
#
# # Получение данных объявления
# response = requests.get("http://127.0.0.1:5000/postings/1")
# print(response.status_code)
# print(response.json())

# # Авторизация пользователя
# s = requests.Session()
# response = s.post(
#     "http://127.0.0.1:5000/login",
#     json={"username": "user_1", "password": "123"},
# )
# print(response.status_code)
# print(response.json())
#
# # # Изменение данных объявления
# response = s.patch(
#     "http://127.0.0.1:5000/postings/1",
#     json={"heading": "Пост 4", "description": "Мой новый пост 4"},
# )
# print(response.status_code)
# print(response.json())

# # Аавторизация пользователя
# s = requests.Session()
# response = s.post(
#     "http://127.0.0.1:5000/login",
#     json={"username": "user_1", "password": "123"},
# )
# print(response.status_code)
# print(response.json())
#
# # Удаление объявления
# response = s.delete("http://127.0.0.1:5000/postings/1")
# print(response.status_code)
# print(response.json())
