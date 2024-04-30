import json

# importa el consumidor de websockets
from channels.generic.websocket import WebsocketConsumer



# definimos el consumidor

# Este es un consumidor síncrono de WebSocket que acepta todas las conexiones,
# recibe mensajes de su cliente y los reenvía al mismo cliente.
# Por ahora, no transmite mensajes a otros clientes en la misma sala.
class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def recive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        self.send(text_data=json.dumps({"message": message}))

