

# vamos a enrutar el consumidor

from django.urls import re_path
from . import consumidor as consumers


# definimos una lista de rutas de WebSocket
websocket_urlpatterns = [
    # esta expresion regular se encarga de enrutar todas las conexiones WebSocket
    # que lleguen a la ruta ws/chat/ a nuestro consumidor ChatConsumer

    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi())
    # aqui consumers es un alias de consumidor.py lo que hace es importar la clase ChatConsumer
    # para que pueda ser utilizada en el archivo routing.py
]