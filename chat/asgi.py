# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# Establece la configuración del entorno para el archivo de configuración de Django.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Obtiene la aplicación ASGI de Django para configurar el servidor.
django_asgi_app = get_asgi_application()


# ---

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
                # Configura un enrutador de URL para las conexiones WebSocket utilizando las rutas definidas en chat/routing.py
                URLRouter(websocket_urlpatterns)
            )
        ),
    }
)