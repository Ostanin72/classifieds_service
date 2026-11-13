from flask import jsonify, request
from flask.views import MethodView
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user

from db import User


class AuthView(MethodView):
    def post(self):
        """
        Вход в систему.
        Ожидает JSON: {"username": "...", "password": "..."}
        """
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Request must be JSON"}), 415

        username = json_data.get("username")
        password = json_data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # 1. Ищем пользователя
        user = request.session.query(User).filter_by(username=username).first()

        # 2. Проверяем существование и пароль
        # Используем check_password_hash, а не hash_password!
        if not user or not check_password_hash(user.password, password):
            # ВАЖНО: Не говорите, что именно неверно (пользователь или пароль)
            # для безопасности. Сообщение общее.
            return jsonify({"error": "Invalid username or password"}), 401

        # 3. Создаем сессию
        # remember=True создаст долгоживущую куку (если нужно)
        login_user(user, remember=True)

        # 4. Возвращаем успех
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 200

    def delete(self):
        """
        Выход из системы (Logout).
        """
        logout_user()
        return jsonify({"message": "Logout successful"}), 200
