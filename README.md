# create-svelte

Everything you need to build a Svelte project, powered by [`create-svelte`](https://github.com/sveltejs/kit/tree/main/packages/create-svelte).

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npm create svelte@latest

# create a new project in my-app
npm create svelte@latest my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.



---

# Ruta

### Objetivos
1. Crear una aplicación web de estudio con funcionalidades de creación y gestión de mazos de tarjetas flash.
2. Implementar preguntas de diferentes tipos (multiple choice, drag and drop, completar) dentro de las tarjetas.
3. Permitir la resolución de tarjetas en tiempo real utilizando websockets.
4. Utilizar una API REST para la gestión de mazos y tarjetas.

### Metas Generales
1. Configurar el entorno de desarrollo.
2. Desarrollar el backend con Django.
3. Implementar websockets con Django Channels.
4. Desarrollar la API REST con Django REST Framework.
5. Desarrollar el frontend con Svelte.
6. Integrar el frontend con el backend utilizando la API REST y websockets.
7. Realizar pruebas y depuración.
8. Desplegar la aplicación.

### Tareas más específicas pertenecientes a las metas

#### 1. Configurar el entorno de desarrollo
- [ ] Instalar Python y Node.js.
- [ ] Crear un entorno virtual para Python.
- [ ] Instalar Django y Django REST Framework.
- [ ] Instalar Django Channels.
- [ ] Configurar Redis como backend para channels.
- [ ] Configurar el entorno de desarrollo para Svelte.

#### 2. Desarrollar el backend con Django
- [ ] Crear un nuevo proyecto de Django.
- [ ] Configurar el proyecto (settings.py, urls.py).
- [ ] Crear aplicaciones (apps) dentro del proyecto para gestionar mazos y tarjetas.

#### 3. Implementar websockets con Django Channels
- [ ] Configurar Django Channels en el proyecto.
- [ ] Configurar el routing de channels.
- [ ] Crear consumidores para manejar la lógica de websockets.
- [ ] Integrar Redis como el canal de capa de comunicación.

#### 4. Desarrollar la API REST con Django REST Framework
- [ ] Crear modelos para mazos y tarjetas.
- [ ] Crear vistas API (views) para mazos y tarjetas.
- [ ] Configurar serializadores (serializers).
- [ ] Configurar rutas para las vistas API.
- [ ] Implementar autenticación y permisos.

#### 5. Desarrollar el frontend con Svelte
- [ ] Configurar un nuevo proyecto con Svelte.
- [ ] Crear componentes básicos de la UI.
- [ ] Configurar el cliente HTTP para consumir la API REST.
- [ ] Configurar la conexión de websockets en Svelte.

#### 6. Integrar el frontend con el backend
- [ ] Consumir la API REST desde Svelte.
- [ ] Implementar la lógica de comunicación en tiempo real usando websockets en Svelte.
- [ ] Gestionar el estado de la aplicación en Svelte.

#### 7. Realizar pruebas y depuración
- [ ] Realizar pruebas unitarias y de integración en el backend.
- [ ] Realizar pruebas de la API REST.
- [ ] Realizar pruebas de la comunicación en tiempo real.
- [ ] Realizar pruebas en el frontend.
- [ ] Depurar errores y mejorar el rendimiento.

#### 8. Desplegar la aplicación
- [ ] Configurar el servidor para el despliegue (nginx, gunicorn, Daphne).
- [ ] Configurar la base de datos en el entorno de producción.
- [ ] Configurar el despliegue de Svelte.
- [ ] Desplegar la aplicación en un servidor (Heroku, AWS, DigitalOcean, etc.).
- [ ] Realizar pruebas en el entorno de producción.

### Checklist de Tareas

#### Lado Cliente (Svelte)
- [ ] Configurar proyecto con Svelte.
- [ ] Crear estructura de carpetas y archivos.
- [ ] Crear componentes de la UI para la gestión de mazos y tarjetas.
- [ ] Implementar cliente HTTP para consumir API REST.
- [ ] Configurar y manejar websockets en Svelte.
- [ ] Crear componentes para tipos de preguntas (multiple choice, drag and drop, completar).
- [ ] Gestionar estado de la aplicación.

#### Lado Servidor (Django)
**App REST:**
- [ ] Crear modelos para mazos y tarjetas.
- [ ] Crear vistas API (views) para mazos y tarjetas.
- [ ] Configurar serializadores (serializers).
- [ ] Configurar rutas de API.
- [ ] Implementar autenticación y permisos.

**App Websocket:**
- [ ] Configurar Django Channels.
- [ ] Configurar routing de channels.
- [ ] Crear consumidores (consumers) para manejar la lógica de resolución de tarjetas en tiempo real.
- [ ] Configurar Redis como backend de channels.

### Detalle de tareas específicas

#### Backend (Django)
1. **Modelos**
    - [ ] Crear modelo `Deck` (mazo) con campos como `title`, `description`, `created_by`.
    - [ ] Crear modelo `Card` (tarjeta) con campos como `deck`, `question_type`, `question`, `options`, `answer`.

2. **Vistas API (Views)**
    - [ ] Crear vista para listar y crear mazos.
    - [ ] Crear vista para listar, crear, actualizar y eliminar tarjetas en un mazo.

3. **Serializadores (Serializers)**
    - [ ] Crear serializador para `Deck`.
    - [ ] Crear serializador para `Card`.

4. **Rutas (URLs)**
    - [ ] Configurar rutas para las vistas de mazos y tarjetas.

5. **Websockets (Django Channels)**
    - [ ] Configurar `routing.py` para channels.
    - [ ] Crear consumidores para manejar eventos en tiempo real (e.g., resolución de tarjetas).
    - [ ] Configurar la capa de comunicación con Redis.

#### Frontend (Svelte)
1. **Estructura del Proyecto**
    - [ ] Configurar estructura básica del proyecto Svelte.
    - [ ] Crear componentes de UI (e.g., `DeckList`, `DeckDetail`, `CardForm`, `CardQuestion`).

2. **Integración con API REST**
    - [ ] Configurar cliente HTTP para consumir la API REST.
    - [ ] Implementar lógica para crear, listar, actualizar y eliminar mazos y tarjetas.

3. **Websockets**
    - [ ] Configurar la conexión de websockets.
    - [ ] Implementar lógica de resolución de tarjetas en tiempo real.
