
---

¡Excelente! ¡Este tutorial es bastante detallado! Vamos a darle un poco más de claridad y estilo para que sea más atractivo y fácil de seguir.

---

**Tutorial Parte 2: Implementar un Servidor de Chat**

Este tutorial da continuidad al Tutorial 1. Vamos a hacer que la página de la sala funcione para que puedas chatear contigo mismo y con otros en la misma sala.

**Agregar la vista de la sala**

Primero, crearemos la segunda vista, una vista de sala que te permite ver los mensajes publicados en una sala de chat específica.

1. Crea un nuevo archivo llamado `room.html` dentro de la carpeta `chat/templates/chat/`.

```html
<!-- chat/templates/chat/room.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Sala de Chat</title>
</head>
<body>
    <textarea id="chat-log" cols="100" rows="20"></textarea><br>
    <input id="chat-message-input" type="text" size="100"><br>
    <input id="chat-message-submit" type="button" value="Enviar">
    {{ room_name|json_script:"room-name" }}
    <script>
        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            document.querySelector('#chat-log').value += (data.message + '\n');
        };

        chatSocket.onclose = function(e) {
            console.error('La conexión del chat se cerró inesperadamente');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.key === 'Enter') {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
    </script>
</body>
</html>
```

2. Crea la función de vista para la vista de la sala en `chat/views.py`:

```python
# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
```

3. Agrega la ruta para la vista de la sala en `chat/urls.py`:

```python
# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
```

**Iniciar el servidor de desarrollo de Channels**

Para iniciar el servidor de desarrollo de Channels, ejecuta el siguiente comando:

```
$ python3 manage.py runserver
```

Ve a http://127.0.0.1:8000/chat/ en tu navegador para ver la página de inicio.

Escribe "lobby" como el nombre de la sala y presiona enter. Deberías ser redirigido a la página de la sala en http://127.0.0.1:8000/chat/lobby/, que ahora muestra un registro de chat vacío.

Escribe el mensaje "hola" y presiona enter. No pasa nada. En particular, el mensaje no aparece en el registro de chat. ¿Por qué?

La vista de la sala está intentando abrir un WebSocket en la URL `ws://127.0.0.1:8000/ws/chat/lobby/` pero aún no hemos creado un consumidor que acepte conexiones WebSocket. Si abres la consola de JavaScript del navegador, deberías ver un error que se ve así:

```
WebSocket connection to 'ws://127.0.0.1:8000/ws/chat/lobby/' failed: Unexpected response code: 500
```

**Escribir tu primer consumidor**

Cuando Django acepta una solicitud HTTP, consulta el URLconf raíz para buscar una función de vista, y luego llama a la función de vista para manejar la solicitud. De manera similar, cuando Channels acepta una conexión WebSocket, consulta la configuración de enrutamiento raíz para buscar un consumidor, y luego llama a varias funciones en el consumidor para manejar eventos desde la conexión.

Escribiremos un consumidor básico que acepte conexiones WebSocket en la ruta `/ws/chat/ROOM_NAME/` que tome cualquier mensaje que reciba en el WebSocket y lo devuelva al mismo WebSocket.

**Crear un nuevo archivo `consumers.py` dentro de la carpeta `chat/`**

```python
# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))
```

Este es un consumidor síncrono de WebSocket que acepta todas las conexiones, recibe mensajes de su cliente y los reenvía al mismo cliente. Por ahora, no transmite mensajes a otros clientes en la misma sala.

**Crear una configuración de enrutamiento para el consumidor en `chat/routing.py`**

```python
# chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
```

Ahora, la configuración de enrutamiento raíz especifica que cuando se realiza una conexión al servidor de desarrollo de Channels, el ProtocolTypeRouter primero inspeccionará el tipo de conexión. Si es una conexión WebSocket (`ws://` o `wss://`), la conexión se enviará a `AuthMiddlewareStack`.



---
