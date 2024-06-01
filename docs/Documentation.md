
# Instalación de Channels

Channels está disponible en PyPI y se puede instalar junto con el servidor de aplicaciones Daphne ASGI. Aquí se detallan los pasos para su instalación y configuración.

#### Instalación Básica

Para instalar Channels junto con Daphne, ejecuta el siguiente comando:

```bash
python -m pip install -U 'channels[daphne]'
```

Esto instalará Channels y el servidor de aplicaciones Daphne ASGI. Si prefieres usar un servidor de aplicaciones diferente, simplemente instala Channels sin la opción `daphne`.

#### Configuración en Django

1. **Agregar Daphne a INSTALLED_APPS**:
   
   Añade `daphne` al principio de tu configuración de `INSTALLED_APPS` en tu archivo `settings.py`:

   ```python
   INSTALLED_APPS = (
       "daphne",
       "django.contrib.auth",
       "django.contrib.contenttypes",
       "django.contrib.sessions",
       "django.contrib.sites",
       ...
   )
   ```

   Esto habilitará la versión ASGI de Daphne en el comando de gestión `runserver`.

2. **Agregar Channels a INSTALLED_APPS**:
   
   También puedes añadir `channels` para habilitar el comando `runworker`:

   ```python
   INSTALLED_APPS += (
       "channels",
   )
   ```

3. **Configurar el archivo `asgi.py`**:
   
   Ajusta tu archivo `asgi.py` (por ejemplo, `myproject/asgi.py`) para envolver la aplicación Django ASGI:

   ```python
   import os
   from channels.routing import ProtocolTypeRouter
   from django.core.asgi import get_asgi_application

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

   # Inicializar la aplicación ASGI de Django temprano para asegurar que el AppRegistry esté poblado
   django_asgi_app = get_asgi_application()

   application = ProtocolTypeRouter({
       "http": django_asgi_app,
       # Solo HTTP por ahora. (Podemos agregar otros protocolos más tarde.)
   })
   ```

4. **Establecer ASGI_APPLICATION**:
   
   Configura tu ajuste `ASGI_APPLICATION` para apuntar a ese objeto de enrutamiento como tu aplicación raíz:

   ```python
   ASGI_APPLICATION = "myproject.asgi.application"
   ```

#### Nota

Ten cuidado con cualquier otra aplicación de terceros que requiera una sobrecarga o sustitución del comando `runserver`. Daphne proporciona un comando `runserver` separado y puede entrar en conflicto con él. Un ejemplo de tal conflicto es con `whitenoise.runserver.nostatic` de Whitenoise. Para resolver estos problemas, asegúrate de que `daphne` esté en la parte superior de tu `INSTALLED_APPS` o elimina por completo la aplicación conflictiva.

### Instalación de la Última Versión de Desarrollo

Para instalar la última versión de Channels, sigue estos pasos:

1. Clona el repositorio:

   ```bash
   $ git clone git@github.com:django/channels.git
   ```

2. Cambia al directorio del repositorio:

   ```bash
   $ cd channels
   ```

3. Activa tu entorno virtual del proyecto y luego instala Channels:

   ```bash
   $ <activa tu entorno virtual>
   (environment) $ pip install -e .  # el punto especifica el repositorio actual
   ```




---


# Parte 1: Configuración Básica

**Nota:** Si encuentra algún problema durante su sesión de codificación, consulte la sección de **Solución de Problemas**.

En este tutorial construiremos un simple servidor de chat con dos páginas:
1. Una vista índice que permite escribir el nombre de una sala de chat para unirse.
2. Una vista de habitación que permite ver mensajes publicados en una sala de chat particular.

La vista de la habitación utilizará un WebSocket para comunicarse con el servidor Django y escuchar cualquier mensaje que se publique.

**Requisitos previos:**
- Familiaridad con conceptos básicos de Django.
- Django instalado (`$ python3 -m django --version`).
- Channels y Daphne instalados (`$ python3 -c 'import channels; import daphne; print(channels.__version__, daphne.__version__)'`).

**Nota:** Este tutorial utiliza Channels 4.0, que soporta Python 3.7 y Django 3.2. También se utiliza Docker para instalar y ejecutar Redis, el almacenamiento de respaldo para la capa de canal.

## Creación de un Proyecto Django

Si no tienes un proyecto Django, créalo con:

```bash
$ django-admin startproject mysite
```

Esto creará un directorio `mysite` con la estructura básica de un proyecto Django.

## Creación de la Aplicación Chat

Desde el directorio del proyecto (`manage.py`), crea la aplicación chat:

```bash
$ python3 manage.py startapp chat
```

Elimina los archivos innecesarios en el directorio `chat` para que solo queden `__init__.py` y `views.py`.

**Estructura del directorio de chat:**
```
chat/
    __init__.py
    views.py
```

Agrega la aplicación `chat` a `INSTALLED_APPS` en `mysite/settings.py`:

```python
# mysite/settings.py
INSTALLED_APPS = [
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

## Añadir la Vista Índice

Crea el directorio de plantillas y la plantilla `index.html`:

```plaintext
chat/
    __init__.py
    templates/
        chat/
            index.html
    views.py
```

**Contenido de `chat/templates/chat/index.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Chat Rooms</title>
</head>
<body>
    What chat room would you like to enter?<br>
    <input id="room-name-input" type="text" size="100"><br>
    <input id="room-name-submit" type="button" value="Enter">

    <script>
        document.querySelector('#room-name-input').focus();
        document.querySelector('#room-name-input').onkeyup = function(e) {
            if (e.key === 'Enter') {
                document.querySelector('#room-name-submit').click();
            }
        };

        document.querySelector('#room-name-submit').onclick = function(e) {
            var roomName = document.querySelector('#room-name-input').value;
            window.location.pathname = '/chat/' + roomName + '/';
        };
    </script>
</body>
</html>
```

**Función de vista para `index` en `chat/views.py`:**
```python
from django.shortcuts import render

def index(request):
    return render(request, "chat/index.html")
```

Crea `chat/urls.py` y mapea la vista `index`:

```python
# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

Apunta la raíz `URLconf` en `mysite/urls.py` para incluir las URLs de chat:

```python
# mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
]
```

Ejecuta el servidor y verifica la vista del índice:

```bash
$ python3 manage.py runserver
```

Visita `http://127.0.0.1:8000/chat/` y verifica que la página de índice funcione. Detén el servidor con `Control-C`.

## Integrar la Biblioteca de Canales

Ajusta `mysite/asgi.py` para incluir la configuración de enrutado para Canales:

```python
# mysite/asgi.py
import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Solo HTTP por ahora. (Podemos agregar otros protocolos más tarde.)
    }
)
```

Agrega `daphne` a `INSTALLED_APPS` en `mysite/settings.py`:

```python
# mysite/settings.py
INSTALLED_APPS = [
    'daphne',
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Configura `ASGI_APPLICATION` en `mysite/settings.py`:

```python
# mysite/settings.py
ASGI_APPLICATION = "mysite.asgi.application"
```

Ejecuta el servidor y verifica que Daphne esté funcionando correctamente:

```bash
$ python3 manage.py runserver
```

Deberías ver una salida indicando que el servidor de desarrollo ASGI/Daphne está corriendo.

Visita `http://127.0.0.1:8000/chat/` para verificar la página de índice. Detén el servidor con `Control-C`.





---




#  Parte 2: Implementar un Servidor de Chat con Django Channels

Este tutorial es la continuación del **Tutorial 1** y te guiará para hacer que la página de la sala funcione para que puedas chatear contigo mismo y con otros en la misma sala.

#### Añadir la Vista de la Sala

1. **Estructura del Proyecto:**
   ```plaintext
   chat/
       __init__.py
       templates/
           chat/
               index.html
               room.html
       urls.py
       views.py
   ```

2. **Plantilla de la Sala:**
   ```html
   <!-- chat/templates/chat/room.html -->
   <!DOCTYPE html>
   <html>
   <head>
       <meta charset="utf-8"/>
       <title>Chat Room</title>
   </head>
   <body>
       <textarea id="chat-log" cols="100" rows="20"></textarea><br>
       <input id="chat-message-input" type="text" size="100"><br>
       <input id="chat-message-submit" type="button" value="Send">
       {{ room_name|json_script:"room-name" }}
       <script>
           const roomName = JSON.parse(document.getElementById('room-name').textContent);
           const chatSocket = new WebSocket(
               'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
           );

           chatSocket.onmessage = function(e) {
               const data = JSON.parse(e.data);
               document.querySelector('#chat-log').value += (data.message + '\n');
           };

           chatSocket.onclose = function(e) {
               console.error('Chat socket closed unexpectedly');
           };

           document.querySelector('#chat-message-input').focus();
           document.querySelector('#chat-message-input').onkeyup = function(e) {
               if (e.key === 'Enter') {
                   document.querySelector('#chat-message-submit').click();
               }
           };

           document.querySelector('#chat-message-submit').onclick = function(e) {
               const messageInputDom = document.querySelector('#chat-message-input');
               const message = messageInputDom.value;
               chatSocket.send(JSON.stringify({ 'message': message }));
               messageInputDom.value = '';
           };
       </script>
   </body>
   </html>
   ```

3. **Vista de la Sala:**
   ```python
   # chat/views.py
   from django.shortcuts import render

   def index(request):
       return render(request, "chat/index.html")

   def room(request, room_name):
       return render(request, "chat/room.html", {"room_name": room_name})
   ```

4. **Rutas:**
   ```python
   # chat/urls.py
   from django.urls import path
   from . import views

   urlpatterns = [
       path("", views.index, name="index"),
       path("<str:room_name>/", views.room, name="room"),
   ]
   ```

5. **Iniciar el Servidor de Desarrollo:**
   ```bash
   $ python3 manage.py runserver
   ```

6. **Verificar la Página de la Sala:**
   - Navega a [http://127.0.0.1:8000/chat/](http://127.0.0.1:8000/chat/).
   - Introduce el nombre de la sala y presiona "Enter".

#### Escribir el Primer Consumidor

1. **Estructura del Proyecto:**
   ```plaintext
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

2. **Consumidor de WebSocket:**
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

3. **Enrutado del Consumidor:**
   ```python
   # chat/routing.py
   from django.urls import re_path
   from . import consumers

   websocket_urlpatterns = [
       re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
   ]
   ```

4. **Configurar ASGI:**
   ```python
   # mysite/asgi.py
   import os
   from channels.auth import AuthMiddlewareStack
   from channels.routing import ProtocolTypeRouter, URLRouter
   from channels.security.websocket import AllowedHostsOriginValidator
   from django.core.asgi import get_asgi_application
   from chat.routing import websocket_urlpatterns

   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
   django_asgi_app = get_asgi_application()

   application = ProtocolTypeRouter({
       "http": django_asgi_app,
       "websocket": AllowedHostsOriginValidator(
           AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
       ),
   })
   ```

5. **Aplicar Migraciones:**
   ```bash
   $ python manage.py migrate
   $ python3 manage.py runserver
   ```

6. **Verificar la Conexión:**
   - Abre [http://127.0.0.1:8000/chat/lobby/](http://127.0.0.1:8000/chat/lobby/).
   - Escribe un mensaje y presiona "Enter".

#### Habilitar una Capa de Canal

1. **Instalar Redis:**
   ```bash
   $ docker run --rm -p 6379:6379 redis:7
   ```

2. **Instalar channels_redis:**
   ```bash
   $ python3 -m pip install channels_redis
   ```

3. **Configurar Redis en settings.py:**
   ```python
   # mysite/settings.py
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

4. **Verificar la Configuración:**
   ```bash
   $ python3 manage.py shell
   >>> import channels.layers
   >>> channel_layer = channels.layers.get_channel_layer()
   >>> from asgiref.sync import async_to_sync
   >>> async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})
   >>> async_to_sync(channel_layer.receive)('test_channel')
   {'type': 'hello'}
   >>> exit()
   ```

5. **Actualizar el Consumidor para Usar la Capa de Canal:**
   ```python
   # chat/consumers.py
   import json
   from asgiref.sync import async_to_sync
   from channels.generic.websocket import WebsocketConsumer

   class ChatConsumer(WebsocketConsumer):
       def connect(self):
           self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
           self.room_group_name = f"chat_{self.room_name}"
           async_to_sync(self.channel_layer.group_add)(
               self.room_group_name, self.channel_name
           )
           self.accept()

       def disconnect(self, close_code):
           async_to_sync(self.channel_layer.group_discard)(
               self.room_group_name, self.channel_name
           )

       def receive(self, text_data):
           text_data_json = json.loads(text_data)
           message = text_data_json["message"]
           async_to_sync(self.channel_layer.group_send)(
               self.room_group_name, {"type": "chat.message", "message": message}
           )

       def chat_message(self, event):
           message = event["message"]
           self.send(text_data=json.dumps({"message": message}))
   ```

6. **Iniciar el Servidor de Desarrollo:**
   ```bash
   $ python3 manage.py runserver
   ```

7. **Probar la Aplicación:**
   - Abre dos pestañas del navegador en [http://127.0.0.1:8000/chat/lobby/](http://127.0.0.1:8000/chat/lobby/).
   - Envía un mensaje desde una pestaña y verifica que aparece en ambas pestañas.

¡Ahora tienes un servidor de chat básico completamente funcional! Continúa con el **Tutorial 3** para seguir mejorando tu aplicación de chat.



----



# Parte 3: Reescribir el servicio de chat como asincrónico

En esta parte del tutorial, convertiremos el `ChatConsumer` sincrónico a una versión asincrónica para mejorar el rendimiento.

#### Reescribiendo el consumidor para ser asincrónico

Actualmente, `ChatConsumer` es sincrónico. Los consumidores sincrónicos son convenientes porque pueden llamar a funciones de E/S sincrónicas, como el acceso a los modelos de Django, sin necesidad de escribir código especial. Sin embargo, los consumidores asincrónicos pueden proporcionar un mayor rendimiento, ya que no necesitan crear hilos adicionales para manejar las solicitudes.

Dado que `ChatConsumer` solo utiliza bibliotecas nativas de asincronía (Channels y la capa de canal) y no accede a los modelos sincrónicos de Django, podemos reescribirlo para que sea asincrónico sin complicaciones.

#### Reescribiendo `ChatConsumer` a asincrónico

Modifiquemos `ChatConsumer` para ser asincrónico. Actualiza el archivo `chat/consumers.py` con el siguiente código:

```python
# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
```

### Explicación de los cambios

1. **Herencia**: `ChatConsumer` ahora hereda de `AsyncWebsocketConsumer` en lugar de `WebsocketConsumer`.
2. **Métodos asincrónicos**: Todos los métodos ahora son `async def` en lugar de `def`.
3. **Uso de `await`**: Se utiliza `await` para llamar a funciones asincrónicas que realizan E/S.
4. **Eliminación de `async_to_sync`**: Ya no es necesario cuando se llaman métodos en la capa del canal.

### Verificación

Verifiquemos que el consumidor para la ruta `/ws/chat/ROOM_NAME/` sigue funcionando correctamente.

1. **Inicia el servidor de desarrollo**:
   ```sh
   $ python3 manage.py runserver
   ```

2. **Prueba en el navegador**:
   - Abre una pestaña del navegador en la página de la habitación en [http://127.0.0.1:8000/chat/lobby/](http://127.0.0.1:8000/chat/lobby/).
   - Abre una segunda pestaña del navegador en la misma página de la habitación.
   - En la segunda pestaña del navegador, escribe el mensaje "hello" y presiona Enter.
   - Deberías ver el mensaje "hello" reflejado en el registro de chat tanto en la segunda pestaña del navegador como en la primera.

Con estos pasos, ahora tienes un servidor de chat completamente asincrónico.

### Próximos pasos

Este tutorial continúa en [Tutorial 4](#) donde se abordarán temas más avanzados y se añadirán más funcionalidades al servidor de chat.

¡Felicitaciones! Has convertido con éxito tu servidor de chat a una versión asincrónica, mejorando así su rendimiento.


----


# Parte 4: Pruebas automatizadas

En esta parte del tutorial, escribiremos pruebas automatizadas para nuestro servidor de chat usando Selenium y Channels. Estas pruebas asegurarán que el servidor de chat funcione correctamente.

#### Instalación de dependencias

Primero, necesitamos instalar Selenium y ChromeDriver. Asegúrate de tener Chrome instalado en tu máquina.

1. **Instalar Selenium**:
    ```sh
    $ python3 -m pip install selenium
    ```

2. **Instalar ChromeDriver**:
   - Descarga ChromeDriver desde [aquí](https://sites.google.com/a/chromium.org/chromedriver/downloads) y asegúrate de que el binario esté en tu `$PATH`.

#### Estructura del proyecto

Asegúrate de que tu directorio `chat` tenga la siguiente estructura:

```
chat/
    __init__.py
    consumers.py
    routing.py
    templates/
        chat/
            index.html
            room.html
    tests.py
    urls.py
    views.py
```

#### Escribir pruebas en `chat/tests.py`

Crea un nuevo archivo `chat/tests.py` y añade el siguiente código:

```python
# chat/tests.py
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True  # emulate StaticLiveServerTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # NOTE: Requires "chromedriver" binary to be installed in $PATH
            cls.driver = webdriver.Chrome()
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        try:
            self._enter_chat_room("room_1")

            self._open_new_window()
            self._enter_chat_room("room_1")

            self._switch_to_window(0)
            self._post_message("hello")
            WebDriverWait(self.driver, 2).until(
                lambda _: "hello" in self._chat_log_value,
                "Message was not received by window 1 from window 1",
            )
            self._switch_to_window(1)
            WebDriverWait(self.driver, 2).until(
                lambda _: "hello" in self._chat_log_value,
                "Message was not received by window 2 from window 1",
            )
        finally:
            self._close_all_new_windows()

    def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        try:
            self._enter_chat_room("room_1")

            self._open_new_window()
            self._enter_chat_room("room_2")

            self._switch_to_window(0)
            self._post_message("hello")
            WebDriverWait(self.driver, 2).until(
                lambda _: "hello" in self._chat_log_value,
                "Message was not received by window 1 from window 1",
            )

            self._switch_to_window(1)
            self._post_message("world")
            WebDriverWait(self.driver, 2).until(
                lambda _: "world" in self._chat_log_value,
                "Message was not received by window 2 from window 2",
            )
            self.assertTrue(
                "hello" not in self._chat_log_value,
                "Message was improperly received by window 2 from window 1",
            )
        finally:
            self._close_all_new_windows()

    # === Utility ===

    def _enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + "/chat/")
        ActionChains(self.driver).send_keys(room_name, Keys.ENTER).perform()
        WebDriverWait(self.driver, 2).until(
            lambda _: room_name in self.driver.current_url
        )

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self._switch_to_window(-1)

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self._switch_to_window(-1)
            self.driver.execute_script("window.close();")
        if len(self.driver.window_handles) == 1:
            self._switch_to_window(0)

    def _switch_to_window(self, window_index):
        self.driver.switch_to.window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message, Keys.ENTER).perform()

    @property
    def _chat_log_value(self):
        return self.driver.find_element(
            by=By.CSS_SELECTOR, value="#chat-log"
        ).get_property("value")
```

#### Configuración de la base de datos para pruebas

Modifica tu archivo `mysite/settings.py` para configurar la base de datos de pruebas. Añade el parámetro `TEST` a la configuración `DATABASES`:

```python
# mysite/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "TEST": {
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
}
```

#### Ejecutar las pruebas

Ejecuta las pruebas con el siguiente comando:

```sh
$ python3 manage.py test chat.tests
```

Deberías ver una salida similar a la siguiente:

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 5.014s

OK
Destroying test database for alias 'default'...
```

### Conclusión

Ahora tienes un servidor de chat completamente probado y asincrónico. Felicidades por completar el tutorial. Con lo aprendido, puedes empezar a crear tus propias aplicaciones utilizando Channels y añadir funcionalidades avanzadas.

¡Buena suerte con tus proyectos futuros!