from todor import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()


'''
**¿Para qué sirve?** Es el **punto de entrada** de la aplicación.  Es el archivo que ejecutarás para iniciar el servidor web.

**¿Por qué separarlo de `__init__.py`?** Separa la lógica de inicialización de la app (en `__init__.py`) de la ejecución (en `run.py`).
'''