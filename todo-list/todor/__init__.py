from flask import Flask
from . import todo
from . import auth

def create_app():
    app = Flask(__name__)

    #Configuracion de la app
    app.config.from_mapping(DEBUG=False, SECRET_KEY='dev')

    #Registrar Blueprint
    app.register_blueprint(todo.bp)
    app.register_blueprint(auth.bp)
    
    
    @app.route('/')
    def index():
        return 'Pagina principal'
    
    
    
    return app

'''
**¿Por qué es importante?**

- *¿Qué hace? ** Convierte el directorio `todor` en un **paquete de Python**.
- Permite importar módulos desde ese directorio: `from todor import create_app`
- Es donde inicializaremos y configuraremos nuestra aplicación Flask
- Centraliza la configuración de la app (base de datos, blueprints, etc.)

**Concepto clave:** Sin `__init__.py`, Python no reconocería `todor` como un paquete importable.
'''