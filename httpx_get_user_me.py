import httpx

# Данные для авторизации
login_payload = {
    "email": "testuser@example.com",
    "password": "password"
}
# Авторизация и получение токена
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

access_token = login_response_data["token"]["accessToken"]

# Получаем данные текущего пользователя
users_me_response = httpx.get(
    "http://localhost:8000/api/v1/users/me",
    headers={"Authorization": f'Bearer {access_token}'}
)
users_me_response_data = users_me_response.json()

# Выводим в консоль данные пользователя и статус код ответа
print("Current user:", users_me_response_data)
print("Status Code:", users_me_response.status_code)

