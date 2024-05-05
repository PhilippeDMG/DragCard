# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Unirse al grupo de la sala
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Aceptar la conexión WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de la sala
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Recibir mensaje desde WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Enviar mensaje al grupo de la sala
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Recibir mensaje desde el grupo de la sala
    async def chat_message(self, event):
        message = event["message"]

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({"message": message}))