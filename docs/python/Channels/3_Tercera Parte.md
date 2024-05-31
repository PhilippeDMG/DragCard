
# **Tutorial Parte 3: Reescribir el Servidor de Chat como Asincrónico**

Este tutorial da continuidad a donde quedó el Tutorial 2. Vamos a reescribir el código del consumidor para que sea asíncrono en lugar de síncrono para mejorar su rendimiento.

## **Reescribir el consumidor para ser asíncrono**

El `ChatConsumer` que hemos escrito actualmente es síncrono. Los consumidores síncronos son convenientes porque pueden llamar a funciones de E/S síncronas regulares, como aquellas que acceden a modelos de Django, sin escribir código especial. Sin embargo, los consumidores asíncronos pueden proporcionar un mayor rendimiento ya que no necesitan crear hilos adicionales al manejar las solicitudes.

El `ChatConsumer` solo utiliza bibliotecas nativas asíncronas (Channels y la capa de canales) y en particular no accede a modelos síncronos de Django. Por lo tanto, puede ser reescrito como asíncrono sin complicaciones.

## **Reescribamos el `ChatConsumer` para que sea asíncrono**

```python
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
```

Este nuevo código para `ChatConsumer` es muy similar al código original, con las siguientes diferencias:

- `ChatConsumer` ahora hereda de `AsyncWebsocketConsumer` en lugar de `WebsocketConsumer`.
- Todos los métodos son `async def` en lugar de solo `def`.
- Se utiliza `await` para llamar a funciones asíncronas que realizan E/S.
- Ya no se necesita `async_to_sync` al llamar a métodos en la capa de canales.

## **Verificación del funcionamiento**

Para iniciar el servidor de desarrollo de Channels, ejecuta el siguiente comando:

```bash
$ python3 manage.py runserver
```

Abre una pestaña del navegador en la página de la sala en [http://127.0.0.1:8000/chat/lobby/](http://127.0.0.1:8000/chat/lobby/). Abre una segunda pestaña del navegador en la misma página de la sala.

En la segunda pestaña del navegador, escribe el mensaje "hola" y presiona enter. Ahora deberías ver "hola" reflejado en el registro de chat tanto en la segunda pestaña del navegador como en la primera.

¡Ahora tu servidor de chat es completamente asíncrono!

Este tutorial continúa en el Tutorial 4.