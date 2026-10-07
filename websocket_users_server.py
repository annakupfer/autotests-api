import asyncio
import websockets

from websockets import ServerConnection

async def echo_users(websocket: ServerConnection):
    async for message in websocket:
        print(f"Получено сообщение от пользователя: {message}")

        for i in range(5):
            response = f"{i+1} Сообщение пользователя: {message}"
            await websocket.send(response)

async def main():
    server = await websockets.serve(echo_users, "localhost", 8765)
    print("WebSocket server is running on ws://localhost:8765")
    await server.wait_closed()

asyncio.run(main())


