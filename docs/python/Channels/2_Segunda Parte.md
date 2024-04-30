
---

¡Excelente! ¡Este tutorial es bastante detallado! Vamos a darle un poco más de claridad y estilo para que sea más atractivo y fácil de seguir.

---

**Tutorial Parte 2: Implementar un Servidor de Chat**

Este tutorial da continuidad al Tutorial 1. Vamos a hacer que la página de la sala funcione para que puedas chatear contigo mismo y con otros en la misma sala.

**Agregar la vista de la sala**

Primero, crearemos la segunda vista, una vista de sala que te permite ver los mensajes publicados en una sala de chat específica.

1. Crea un nuevo archivo llamado `room.html` dentro de la carpeta `chat/templates/chat/`.
Este código HTML y JavaScript forma parte de un cliente de chat en tiempo real usando Django Channels. A continuación, te proporcionaré comentarios línea por línea para explicar lo que hace cada parte, especialmente la parte de scripts:

```html
<!-- chat/templates/chat/room.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Sala de Chat</title>
</head>
<body>
    <!-- Un área de texto para mostrar el historial del chat -->
    <textarea id="chat-log" cols="100" rows="20"></textarea><br>
    <!-- Un campo de entrada de texto para escribir mensajes -->
    <input id="chat-message-input" type="text" size="100"><br>
    <!-- Un botón para enviar mensajes -->
    <input id="chat-message-submit" type="button" value="Enviar">
    <!-- Un script que contiene información sobre la sala de chat, serializada en JSON -->
    {{ room_name|json_script:"room-name" }}
    <script>
        // Parsea la información de la sala de chat desde el script JSON
        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        // Crea un WebSocket para la comunicación bidireccional con el servidor
        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host  // La dirección del host actual
            + '/ws/chat/'  // La ruta para el WebSocket en Django Channels
            + roomName  // El nombre de la sala de chat, usado como identificador único
            + '/'
        );

        // Función que se ejecuta cuando el cliente recibe un mensaje del servidor
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);  // Parsea el mensaje JSON recibido
            document.querySelector('#chat-log').value += (data.message + '\n');  // Agrega el mensaje al historial del chat
        };

        // Función que se ejecuta cuando la conexión WebSocket se cierra inesperadamente
        chatSocket.onclose = function(e) {
            console.error('La conexión del chat se cerró inesperadamente');
        };

        // Enfoca el campo de entrada de texto para escribir mensajes
        document.querySelector('#chat-message-input').focus();
        // Maneja el evento keyup (tecla presionada) en el campo de entrada de texto
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.key === 'Enter') {  // Si la tecla presionada es Enter
                document.querySelector('#chat-message-submit').click();  // Simula un clic en el botón de enviar mensaje
            }
        };

        // Maneja el evento click en el botón de enviar mensaje
        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');  // Obtiene el campo de entrada de texto
            const message = messageInputDom.value;  // Obtiene el mensaje ingresado por el usuario
            chatSocket.send(JSON.stringify({  // Envía el mensaje al servidor, serializado en JSON
                'message': message  // El mensaje en sí
            }));
            messageInputDom.value = '';  // Limpia el campo de entrada de texto después de enviar el mensaje
        };
    </script>
</body>
</html>
```

La parte de scripts en este caso específico toma la variable `room_name`, que probablemente sea un string, y la serializa en formato JSON. Luego, esa información se inserta en un script dentro del HTML, lo que permite que el JavaScript acceda a esa información y la utilice para crear el WebSocket necesario para la comunicación con el servidor de Django Channels.

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

## **Escribe tu primer consumidor**

Cuando Django acepta una solicitud HTTP, consulta el URLconf raíz para buscar una función de vista, y luego llama a la función de vista para manejar la solicitud. De manera similar, cuando Channels acepta una conexión WebSocket, consulta la configuración de enrutamiento raíz para buscar un consumidor, y luego llama a varias funciones en el consumidor para manejar eventos desde la conexión.

Vamos a escribir un consumidor básico que acepta conexiones WebSocket en la ruta /ws/chat/ROOM_NAME/ y que toma cualquier mensaje que recibe en el WebSocket y lo devuelve al mismo WebSocket.

**Crea un nuevo archivo chat/consumers.py.** Tu directorio de la aplicación debería lucir así:

```
chat/
    __init__.py
    consumers.py
    templates/
        chat/
            index.html
            room.html
    urls.py
    views.py
```

Coloca el siguiente código en chat/consumers.py:

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

Este es un consumidor síncrono de WebSocket que acepta todas las conexiones, recibe mensajes de su cliente y ecoa esos mensajes de vuelta al mismo cliente. Por ahora, no difunde mensajes a otros clientes en la misma sala.

Ahora necesitamos crear una configuración de enrutamiento para la aplicación de chat que tenga una ruta hacia el consumidor. Crea un nuevo archivo chat/routing.py. Tu directorio de la aplicación debería lucir así:

```
chat/
    __init__.py
    consumers.py
    routing.py
    templates/
        chat/
            index.html
            room.html
    urls.py
    views.py
```

Coloca el siguiente código en chat/routing.py:

```python
# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
```

Llamamos al método de clase `as_asgi()` para obtener una aplicación ASGI que instanciará una instancia de nuestro consumidor para cada conexión de usuario. Esto es similar a `as_view()` de Django, que cumple el mismo papel para las instancias de vista de Django por solicitud.

(Nota que usamos `re_path()` debido a limitaciones en `URLRouter`).

El siguiente paso es apuntar la configuración ASGI principal al módulo chat.routing. En mysite/asgi.py, importa `AuthMiddlewareStack`, `URLRouter` y `chat.routing`, e inserta una clave 'websocket' en el listado `ProtocolTypeRouter` en el siguiente formato:
Este fragmento de código es el archivo `asgi.py` que se utiliza para configurar el servidor ASGI en una aplicación Django Channels. Aquí hay una explicación detallada de lo que hace cada parte del código:

```python
# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# Establece la configuración del entorno para el archivo de configuración de Django.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Obtiene la aplicación ASGI de Django para configurar el servidor.
django_asgi_app = get_asgi_application()

# Importa las rutas de WebSocket de la aplicación de chat.
from chat.routing import websocket_urlpatterns

# Configura el enrutador de protocolo para el servidor ASGI.
application = ProtocolTypeRouter(
    {
        # Maneja las conexiones HTTP usando la aplicación ASGI de Django.
        "http": django_asgi_app,
        # Maneja las conexiones WebSocket.
        "websocket": AllowedHostsOriginValidator(
            # Agrega una capa de autenticación de middleware para las conexiones WebSocket.
            AuthMiddlewareStack(
                # Configura un enrutador de URL para las conexiones WebSocket utilizando las rutas definidas en chat.routing.
                URLRouter(websocket_urlpatterns)
            )
        ),
    }
)
```

#### Explicación detallada

- `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")`: Establece la configuración del entorno para que Django pueda encontrar el archivo de configuración de la aplicación.

- `django_asgi_app = get_asgi_application()`: Obtiene la aplicación ASGI de Django para configurar el servidor ASGI.

- `from chat.routing import websocket_urlpatterns`: Importa las rutas de WebSocket definidas en el archivo de enrutamiento de la aplicación de chat.

- `application = ProtocolTypeRouter(...)`: Configura el enrutador de protocolo para el servidor ASGI. Este enrutador se encarga de enrutar las conexiones HTTP y WebSocket a sus respectivos controladores.

  - `"http": django_asgi_app`: Define que las conexiones HTTP deben ser manejadas por la aplicación ASGI de Django.

  - `"websocket": ...`: Define que las conexiones WebSocket deben ser manejadas por el código proporcionado a continuación.

  - `AllowedHostsOriginValidator`: Un validador de seguridad que garantiza que las conexiones WebSocket provengan de hosts permitidos.

  - `AuthMiddlewareStack`: Agrega una capa de middleware para autenticación de usuarios a las conexiones WebSocket.

  - `URLRouter(websocket_urlpatterns)`: Configura un enrutador de URL para las conexiones WebSocket utilizando las rutas definidas en `chat.routing`. Estas rutas se utilizan para enrutar las conexiones WebSocket a los consumidores adecuados.
Esta configuración de enrutamiento raíz especifica que cuando se realiza una conexión al servidor de desarrollo de Channels, el ProtocolTypeRouter primero inspeccionará el tipo de conexión. Si es una conexión WebSocket (ws:// o wss://), la conexión se enviará a `AuthMiddlewareStack`.


`AuthMiddlewareStack` llenará el ámbito de la conexión con una referencia al usuario actualmente autenticado, similar a cómo `AuthenticationMiddleware` de Django llena el objeto de solicitud de una función de vista con el usuario actualmente autenticado. Luego, la conexión se enviará a `URLRouter`.

`URLRouter` examinará la ruta HTTP de la conexión para enrutarlo a un consumidor específico, según los patrones de URL proporcionados.

**Verifiquemos que el consumidor para la ruta /ws/chat/ROOM_NAME/ funcione.** Ejecuta las migraciones para aplicar los cambios en la base de datos (el framework de sesiones de Django necesita la base de datos) y luego inicia el servidor de desarrollo de Channels:

```
$ python manage.py migrate
```

Luego, para iniciar el servidor de desarrollo:

```
$ python3 manage.py runserver
```

Ve a la página de la sala en http://127.0.0.1:8000/chat/lobby/, la cual ahora muestra un registro de chat vacío.

Escribe el mensaje “hola” y presiona enter. Ahora deberías ver “hola” reflejado en el registro de chat.

Sin embargo, si abres una segunda pestaña del navegador en la misma página de la sala en http://127.0.0.1:8000/chat/lobby/ y escribes un mensaje, el mensaje no aparecerá en la primera pestaña. Para que eso funcione, necesitamos tener múltiples instancias del mismo ChatConsumer capaces de hablar entre sí. Channels proporciona una abstracción de capa de canal que permite este tipo de comunicación entre consumidores.

Ve a la terminal donde ejecutaste el comando runserver y presiona Control-C para detener el servidor.

**Habilitar una capa de canal**

Una capa de canal es un tipo de sistema de comunicación que permite que múltiples instancias de consumidores hablen entre sí y con otras partes de Django.

Una capa de canal proporciona las siguientes abstracciones:

- Un canal es un buzón donde se pueden enviar mensajes. Cada canal tiene un nombre. Cualquiera que tenga el nombre de un canal puede enviar un mensaje al canal.

- Un grupo es un conjunto de canales relacionados. Un grupo tiene un nombre. Cualquiera que tenga el nombre de un grupo puede agregar/eliminar un canal al grupo por nombre y enviar un mensaje a todos los canales en el grupo. No es posible enumerar qué canales están en un grupo particular.

Cada instancia de consumidor tiene un nombre de canal único generado automáticamente, y por lo tanto puede comunicarse a través de una capa de canal.

En nuestra aplicación de chat, queremos que múltiples instancias de `ChatConsumer` en la misma sala se comuniquen entre sí. Para hacer eso, cada `ChatConsumer` agregará su canal a un grupo cuyo nombre se basa en el nombre de la sala. Eso permitirá que los `ChatConsumers` transmitan mensajes a todos los otros `ChatConsumers` en la misma sala.

Utilizaremos una capa de canal que utilice Redis como su almacén de respaldo. Para iniciar un servidor Redis en el puerto 6379, ejecuta el siguiente comando (presiona Control-C para detenerlo):

```
$ docker run --rm -p 6379:6379 redis:7
```

Necesitamos instalar `channels_redis` para que Channels sepa cómo interactuar con Redis. Ejecuta el siguiente comando:

```
$ python3 -m pip install channels_redis
```

Antes de poder usar una capa de canal, debemos configurarla. Edita el archivo mysite/settings.py y agrega una configuración `CHANNEL_LAYERS` al final. Debería lucir así:

```python
# mysite/settings.py
# Channels
ASGI_APPLICATION = "mysite.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

**Nota:**
Es posible tener múltiples capas de canal configuradas. Sin embargo, la mayoría de los proyectos solo usarán una capa de canal 'default'.

Verifiquemos que la capa de canal pueda comunicarse con Redis. Abre un shell de Django y ejecuta los siguientes comandos:

```
$ python3 manage.py shell
```

```python
import channels.layers

channel_layer = channels.layers.get_channel_layer()

from asgiref.sync import async_to_sync

async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})

async_to_sync(channel_layer.receive)('test_channel')
{'type': 'hello'}
```

Escribe Control-D para salir del shell de Django.

Ahora que tenemos una capa de canal, vamos a usarla en `ChatConsumer`. Coloca el siguiente código en chat/consumers.py, reemplazando el código anterior:

```python
# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


```

Cuando un usuario publica un mensaje, una función de JavaScript transmitirá el mensaje a través de WebSocket a un `ChatConsumer`. El `ChatConsumer` recibirá ese mensaje y lo enviará al grupo correspondiente al nombre de la sala. Cada `ChatConsumer` en el mismo grupo (y por lo tanto en la misma sala) recibirá el mensaje del grupo y lo enviará de nuevo a través de WebSocket de vuelta a JavaScript, donde se agregará al registro de chat.

Varias partes del nuevo código de `ChatConsumer` merecen una explicación adicional:

- `self.scope["url_route"]["kwargs"]["room_name"]`: Obtiene el parámetro 'room_name' de la ruta URL en chat/routing.py que abrió la conexión WebSocket al consumidor.

- `self.room_group_name = f"chat_{self.room_name}"`: Construye un nombre de grupo Channels directamente a partir del nombre de sala especificado por el usuario, sin ningún tipo de comillas o escapado.

- `async_to_sync(self.channel_layer.group_add)(...)`: Se une a un grupo. El envoltorio `async_to_sync(...)` es necesario porque `ChatConsumer` es un `WebsocketConsumer` síncrono, pero está llamando a un método asíncrono de la capa de canal.

- `self.accept()`: Acepta la conexión WebSocket. Si no llamas a `accept()` dentro del método `connect()`, la conexión será rechazada y cerrada.

- `async_to_sync(self.channel_layer.group_discard)(...)`: Abandona un grupo.

- `async_to_sync(self.channel_layer.group_send)`: Envía un evento a un grupo.

Verifiquemos que el nuevo consumidor para la ruta /ws/chat/ROOM_NAME/ funcione. Para iniciar el servidor de desarrollo de Channels, ejecuta el siguiente comando:

```
$ python3 manage.py runserver
```

Abre una pestaña del navegador

 en la página de la sala en http://127.0.0.1:8000/chat/lobby/. Abre una segunda pestaña del navegador en la misma página de la sala.

En la segunda pestaña del navegador, escribe el mensaje "hello" y presiona enter. Ahora deberías ver "hello" reflejado en el registro de chat en ambas pestañas del navegador.

¡Ahora tienes un servidor de chat básico y completamente funcional!
---
