
# asgi.py es un archivo que se encarga de configurar el protocolo de inicio de la aplicacion
# de django, en este caso se va a configurar para que pueda manejar conexiones WebSocket

import os
# AuthMiddlewareStack es un middleware que se encarga de manejar la autenticacion de los usuarios
from channels.auth import AuthMiddlewareStack

# URLRouter es un enrutador que se encarga de enrutar las conexiones WebSocket
from channels.routing import ProtocolTypeRouter, URLRouter

# AllowedHostsOriginValidator es un validador de origen que solo permite conexiones de hosts permitidos.
from channels.security.websocket import AllowedHostsOriginValidator

# get_asgi_application es una funcion que se encarga de devolver la configuracion 
# de inicio de la aplicacion de django
from django.core.asgi import get_asgi_application

# se importa la lista de rutas de WebSocket
from my_ws_app.routing import websocket_urlpatterns as ws_urlpatterns



# lo que hace DJANGO_SETTINGS_MODULE es decirle a django que archivo de configuracion va a usar
# en este caso core.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


# aqui django_asgi_app guarda la configuracion de inicio de la aplicacion de django
django_asgi_app = get_asgi_application()

# aqui se define el protocolo que se va a usar
application = ProtocolTypeRouter({
    
    
    # en este caso se va a usar http, por lo que se le pasa la configuracion de django_asgi_app
    'http': django_asgi_app,

    # en este caso se va a usar websocket, por lo que se le pasa la configuracion de ws_urlpatterns
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                ws_urlpatterns
            )
        )
    ),
})

