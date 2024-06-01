
# consumidor de websocket


import json

# importamos el decorador async_to_sync
# para convertir funciones asincronas en sincronas
from asgiref.sync import async_to_sync

# importamos la clase WebsocketConsumer
from channels.generic.websocket import WebsocketConsumer



class ChatConsumer(WebsocketConsumer):

    # metodo para conectarse al grupo de chat
    def connect(self):
        # obtenemos el nombre de la sala
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        # creamos el nombre del grupo de chat
        self.room_group_name = f"chat_{self.room_name}"

        # nos unimos al grupo de chat
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )


        # aceptamos la conexion
        self.accept()


    # metodo para desconectarse del grupo de chat
    def disconnect(self, close_code):

        # nos salimos del grupo de chat
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # metodo para recibir mensajes del cliente, luego los envia al grupo de chat
    def receive(self, text_data):

        # convertimos el mensaje a json        
        text_data_json = json.loads(text_data)

        # obtenemos el mensaje
        message = text_data_json["message"]

        # enviamos el mensaje al grupo de chat
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )


    # metodo para enviar mensajes, recibe del grupo de chat y los manda al websocket
    def chat_message(self, event):

        # obtenemos el mensaje
        message = event["message"]

        # enviamos el mensaje al websocket
        self.send(text_data=json.dumps({"message": message}))