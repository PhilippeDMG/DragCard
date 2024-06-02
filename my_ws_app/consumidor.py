
import json

# importamos la clase AsyncWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    # metodo que se ejecuta cuando un cliente se conecta al servidor
    async def connect(self):

        # obtenemos el nombre de la sala
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]        
        self.room_group_name = f"chat_{self.room_name}"

        # unimos al cliente a la sala
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # aceptamos la conexion
        await self.accept()


    # metodo que se ejecuta cuando un cliente se desconecta del servidor
    async def disconnect(self, close_code):

        # sacamos al cliente de la sala
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    # metodo que se ejecuta cuando el servidor recibe un mensaje del cliente
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        browser = text_data_json["browser"]

        # Ahora puedes usar 'browser' como quieras. Por ejemplo, podrías enviarlo de vuelta al cliente:
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "browser": browser
            }
        )


    # metodo que se ejecuta cuando el servidor envia un mensaje a la sala
    async def chat_message(self, event):

        # obtenemos el mensaje
        message = event["message"]
        browser = event["browser"]

        # enviamos el mensaje al cliente a través del websocket
        await self.send(text_data=json.dumps(
            {"message": message, "browser": browser}
        ))



'''

self.room_name: 
    Es el nombre de la sala de chat a la que el cliente se une.
    Se obtiene de la URL de la solicitud WebSocket.

self.room_group_name: 
    Es el nombre del grupo de chat. 
    Se crea a partir del room_name. 
    En Django Channels, un grupo es un canal
    que puede tener múltiples oyentes.
    
'''