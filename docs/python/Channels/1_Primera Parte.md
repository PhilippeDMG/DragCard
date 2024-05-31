
## Construyendo un Servidor de Chat con Django y Channels

En este tutorial, construiremos un servidor de chat simple que consta de dos páginas:

1. Una vista de índice que te permite escribir el nombre de una sala de chat para unirte.
2. Una vista de sala que te permite ver los mensajes publicados en una sala de chat en particular.

La vista de sala utilizará un WebSocket para comunicarse con el servidor de Django y escuchar cualquier mensaje que se publique.

### Requisitos previos

Asumimos que estás familiarizado con los conceptos básicos para construir un sitio web con Django. Si no es así, te recomendamos que completes primero el tutorial de Django y luego regreses aquí.

También asumimos que ya tienes Django, Channels y Daphne instalados. Puedes verificar ejecutando los siguientes comandos:

```bash
$ python3 -m django --version
$ python3 -c 'import channels; import daphne; print(channels.__version__, daphne.__version__)'
```

Este tutorial está escrito para Channels 4.0, que es compatible con Python 3.7+ y Django 3.2+. Si la versión de Channels no coincide, puedes consultar el tutorial para tu versión de Channels utilizando el conmutador de versión en la esquina inferior izquierda de esta página, o actualizar Channels a la versión más nueva.

### Creando un proyecto

Si aún no tienes un proyecto de Django, necesitarás crear uno. Desde la línea de comandos, ingresa al directorio donde te gustaría almacenar tu código y ejecuta el siguiente comando:

```bash
$ django-admin startproject mysite
```

Esto creará un directorio llamado `mysite` en tu directorio actual con la estructura de archivos estándar de Django.

### Creando la aplicación de chat

Crearemos la aplicación de chat en su propio directorio. Asegúrate de estar en el mismo directorio que `manage.py` y escribe el siguiente comando:

```bash
$ python3 manage.py startapp chat
```

Esto creará un directorio llamado `chat`, que contendrá los archivos de nuestra aplicación.

### Eliminando archivos innecesarios

Para simplificar nuestro proyecto, eliminaremos algunos archivos generados automáticamente por Django. Después de eliminarlos, el directorio `chat` debería verse así:

```
chat/
    __init__.py
    views.py
```

### Configurando la aplicación

Necesitamos informar a nuestro proyecto que la aplicación de chat está instalada. Edita el archivo `mysite/settings.py` y agrega `'chat'` a la configuración `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    'chat',
    # otras aplicaciones
]
```

### Añadiendo la vista de índice

Ahora crearemos la primera vista, una vista de índice que te permite escribir el nombre de una sala de chat para unirte.

Crea un directorio `templates` en el directorio `chat`. Dentro del directorio `templates`, crea otro directorio llamado `chat`, y dentro de ese crea un archivo llamado `index.html` para contener la plantilla para la vista de índice.

```html
<!-- chat/templates/chat/index.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Chat Rooms</title>
</head>
<body>
    ¿A qué sala de chat te gustaría unirte?<br>
    <input id="room-name-input" type="text" size="100"><br>
    <input id="room-name-submit" type="button" value="Unirse">

    <script>
        document.querySelector('#room-name-input').focus();
        document.querySelector('#room-name-input').onkeyup = function(e) {
            if (e.key === 'Enter') {  // enter, return
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


---

### Creando la vista y la URL

Ahora necesitamos crear la función de vista para la vista de índice y vincularla a una URL.

En el archivo `chat/views.py`, añade lo siguiente:

```python
# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, "chat/index.html")
```

Para llamar a la vista, necesitamos mapearla a una URL. Creamos un archivo `urls.py` en el directorio `chat` y añadimos el siguiente código:

```python
# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

Ahora, para que Django encuentre nuestras URLs, necesitamos apuntar el URLconf raíz al módulo `chat.urls`. En `mysite/urls.py`, hacemos lo siguiente:

```python
# mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
]
```

### Verificación y Configuración de Channels

Hasta este punto, hemos creado una aplicación de Django básica. Ahora es el momento de integrar Channels.

Comencemos creando una configuración de enrutamiento para Channels. Un enrutamiento de Channels es una aplicación ASGI similar a un URLconf de Django, que le dice a Channels qué código ejecutar cuando recibe una solicitud HTTP.

Ajusta el archivo `mysite/asgi.py` con el siguiente código:

```python
# mysite/asgi.py
import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Solo HTTP por ahora. (Podemos agregar otros protocolos más tarde).
    }
)
```

Luego, añade la biblioteca Daphne a la lista de aplicaciones instaladas en `mysite/settings.py`:

```python
# mysite/settings.py
INSTALLED_APPS = [
    'daphne',
    'chat',
    # otras aplicaciones
]
```

Y apunta Daphne a la configuración de enrutamiento raíz. Añade la siguiente línea al final de `mysite/settings.py`:

```python
# mysite/settings.py
# Daphne
ASGI_APPLICATION = "mysite.asgi.application"
```

### Verificación de Channels

Verifiquemos que el servidor de desarrollo de Channels esté funcionando correctamente. Ejecuta el siguiente comando:

```bash
$ python3 manage.py runserver
```

Deberías ver una salida similar a esta:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
August 19, 2022 - 10:20:28
Django version 4.1, using settings 'mysite.settings'
Starting ASGI/Daphne version 3.0.2 development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Ve a http://127.0.0.1:8000/chat/ en tu navegador y deberías seguir viendo la página de índice que creamos anteriormente.

### Conclusión

Ahora has integrado con éxito Channels en tu proyecto de Django y has creado una página de índice para unirse a las salas de chat. En el siguiente tutorial, continuaremos con la creación de la vista de sala y la comunicación en tiempo real a través de WebSockets.

¡Espero que estas instrucciones sean útiles para ti! ¿Hay algo más en lo que pueda ayudarte?