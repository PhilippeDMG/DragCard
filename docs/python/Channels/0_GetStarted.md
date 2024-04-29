

---

¡Entendido! Empecemos desde el principio.

### Parte 1: Configuración básica

#### Paso 1: Instalación de Channels y Daphne
1. Instala Channels y Daphne ejecutando el siguiente comando:
   ```
   python -m pip install -U 'channels[daphne]'
   ```

#### Paso 2: Configuración del proyecto
1. Añade 'daphne' a la lista de aplicaciones instaladas en el archivo `settings.py`:
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

2. Añade la siguiente configuración al final del archivo `settings.py` para especificar la aplicación ASGI:
   ```python
   # mysite/settings.py
   ASGI_APPLICATION = "mysite.asgi.application"
   ```

3. Ajusta el archivo `asgi.py` para incluir la configuración de enrutamiento de Channels:
   ```python
   # mysite/asgi.py
   import os

   from channels.routing import ProtocolTypeRouter
   from django.core.asgi import get_asgi_application

   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

   application = ProtocolTypeRouter(
       {
           "http": get_asgi_application(),
           # Solo HTTP por ahora. (Podemos agregar otros protocolos más tarde)
       }
   )
   ```

#### Paso 3: Creación del proyecto y la aplicación de chat
1. Crea un proyecto Django ejecutando el siguiente comando:
   ```
   django-admin startproject mysite
   ```

2. Crea una aplicación de chat ejecutando el siguiente comando:
   ```
   python3 manage.py startapp chat
   ```

3. Dentro del directorio de la aplicación de chat, crea una carpeta llamada `templates` y dentro de ella otra carpeta llamada `chat`. Dentro de esta última, crea un archivo llamado `index.html` y coloca el código HTML proporcionado en el tutorial.

4. Crea una vista de índice en el archivo `views.py` de la aplicación de chat con el código proporcionado en el tutorial.

5. Crea un archivo llamado `urls.py` dentro del directorio de la aplicación de chat y coloca el código de configuración de URL proporcionado en el tutorial.

6. Añade la URL de la aplicación de chat al archivo `urls.py` del proyecto.

### Paso 4: Verificación y prueba
1. Ejecuta el servidor de desarrollo Django:
   ```
   python3 manage.py runserver
   ```

2. Abre tu navegador y ve a http://127.0.0.1:8000/chat/ para verificar que la vista de índice se muestre correctamente.

3. Detén el servidor presionando Ctrl + C en la terminal.

¡Esto debería completar la parte 1 del tutorial! ¿Cómo te fue con estos pasos?