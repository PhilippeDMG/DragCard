

Aquí tienes la primera parte traducida al español y formateada en Markdown para Obsidian:

# **Tutorial Parte 4: Pruebas Automatizadas**

Este tutorial comienza donde terminó el Tutorial 3. Hemos construido un servidor de chat simple y ahora crearemos algunas pruebas automatizadas para él.

## **Pruebas de las vistas**

Para asegurarnos de que el servidor de chat siga funcionando, escribiremos algunas pruebas.

Escribiremos una serie de pruebas de extremo a extremo utilizando Selenium para controlar un navegador web Chrome. Estas pruebas asegurarán que:

- Cuando se publica un mensaje de chat, es visto por todos en la misma sala.
- Cuando se publica un mensaje de chat, no es visto por nadie en una sala diferente.

Instala el navegador web Chrome, si aún no lo tienes.

Instala **chromedriver**.

Instala **Selenium**. Ejecuta el siguiente comando:

```bash
$ python3 -m pip install selenium
```

Crea un nuevo archivo `chat/tests.py`. Tu directorio de la aplicación debería verse ahora así:

```plaintext
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



Coloca el siguiente código en `chat/tests.py`:

```python
# chat/tests.py
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True  # emular StaticLiveServerTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # NOTA: Requiere que el binario "chromedriver" esté instalado en $PATH
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

    # === Utilidades ===

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



Aquí tienes la tercera parte traducida y formateada en Markdown para Obsidian:

```markdown
---
tags: [tutorial, testing, chat]
---

Nuestra suite de pruebas extiende `ChannelsLiveServerTestCase` en lugar de las suites usuales de Django para pruebas de extremo a extremo (`StaticLiveServerTestCase` o `LiveServerTestCase`) para que las URLs dentro de la configuración de enrutamiento de Channels como `/ws/room/ROOM_NAME/` funcionen dentro de la suite.

Estamos utilizando `sqlite3`, que para las pruebas se ejecuta como una base de datos en memoria, y por lo tanto, las pruebas no se ejecutarán correctamente. Necesitamos decirle a nuestro proyecto que la base de datos `sqlite3` no necesita estar en memoria para ejecutar las pruebas. Edita el archivo `mysite/settings.py` y añade el argumento `TEST` a la configuración de `DATABASES`:

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

Para ejecutar las pruebas, ejecuta el siguiente comando:

```bash
$ python3 manage.py test chat.tests
```

Deberías ver una salida que se parece a:

```plaintext
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 5.014s

OK
Destroying test database for alias 'default'...
```

¡Ahora tienes un servidor de chat probado!

## ¿Qué sigue?

¡Felicidades! Has implementado completamente un servidor de chat, lo has hecho más eficiente escribiéndolo en estilo asíncrono y has escrito pruebas automatizadas para asegurar que no se rompa.

Este es el final del tutorial. En este punto, deberías saber lo suficiente para comenzar una aplicación propia que use Channels y empezar a experimentar. A medida que necesites aprender nuevos trucos, vuelve al resto de la documentación.


---
