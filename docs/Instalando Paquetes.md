
---

# Django: Entorno y Seguridad

---

Lo primero que hice fue inicializar un proyecto de Django.

```python
asgiref==3.8.1
Django==5.0.3
django-ckeditor==6.7.1
django-cors-headers==4.3.1
django-environ==0.11.2
django-js-asset==2.2.0
django-storages==1.14.2
djangorestframework==3.15.1
pillow==10.2.0
psycopg2-binary==2.9.9
sqlparse==0.4.4
```

- **asgiref**: El framework Django.
- **Django**: Para que el texto y cosas que se publiquen se vean más lindos.
- **django-ckeditor**: Una app de Django para que se pueda comunicar con otros servidores.
- **django-cors-headers**: Entorno para cuidar las claves de seguridad que proporciona Django. Este es especial porque además se crea un archivo .env que es local. Ahí se guarda todo en variables; después, en `settings.py`, se llama a esas variables.
- **django-environ**: Para trabajar con PostgreSQL.
- **django-js-asset**: Nos permite crear API REST y poder comunicarnos directamente con el servidor a través de APIs siguiendo la arquitectura REST.
- **django-storages**: Imágenes en base de datos.
- **djangorestframework**: Para trabajar con PostgreSQL.
- **pillow**: Para trabajar con PostgreSQL.
- **psycopg2-binary**: Para trabajar con PostgreSQL.
- **sqlparse**: Para trabajar con PostgreSQL.

---

Etiquetas: #Django #Seguridad