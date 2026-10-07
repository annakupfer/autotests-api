import httpx

# response = httpx.get("https://jsonplaceholder.typicode.com/todos/1")
# print(response.status_code)  # 200
# print(response.json())
#
#
# data = {
#     "title": "Новая задача",
#     "completed": False,
#     "userId": 1
# }
#
# response = httpx.post("https://jsonplaceholder.typicode.com/todos", json=data)
#
# print(response.status_code)
# print(response.json())
#
# data = {"username": "test_user", "password": "123456"}
# response = httpx.post("https://httpbin.org/post", data=data)
# print(response.status_code)
# print(response.json())
#
# headers = {"Authorization": f"Bearer my_token"}
# response = httpx.get("https://httpbin.org/get", headers=headers)
# print(response.status_code)
# print(response.request.headers)
# print(response.json())
#
# params = {"userId": 1}
# response = httpx.get("https://jsonplaceholder.typicode.com/todos", params=params)
# print(response.status_code)
# print(response.url)
# print(response.json())
#
# files = {"example.txt": open("example.txt", "rb")}
# response = httpx.post("https://httpbin.org/post", files=files)
# print(response.status_code)
# print(response.json())
#
# client = httpx.Client(
#     headers={"Authorization": f"Bearer my_token"}
# )
# response = client.get("https://httpbin.org/get")
# print(response.status_code)
# print(response.json())

try:
    response = httpx.get("https://jsonplaceholder.typicode.com/invalid-url")
    response.raise_for_status()
    print(response.status_code)
except httpx.HTTPStatusError as e:
    print(f"Ошибка запроса: {e} ")


try:
    response = httpx.post("https://httpbin.org/delay/5", timeout=2)
except httpx.ReadTimeout:
    print("Запрос превысил лимит времени")



