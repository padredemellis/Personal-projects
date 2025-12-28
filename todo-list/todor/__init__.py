from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from . import todo
from . import auth

#crear una instancia o extension de sql-alchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #Configuracion de la app
    app.config.from_mapping(DEBUG=False,
     SECRET_KEY='dev',
     SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"
    )

    
    db.init_app(app) #Con esto inicializamos la conexion con nuestra base de datos

    from . import models
    
    #Registrar Blueprint
    app.register_blueprint(todo.bp)
    app.register_blueprint(auth.bp)
    
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    #Migrar los modelos
    with app.app_context():
        db.create_all()
    
    
    
    return app

'''
**¿Por qué es importante?**

- *¿Qué hace? ** Convierte el directorio `todor` en un **paquete de Python**.
- Permite importar módulos desde ese directorio: `from todor import create_app`
- Es donde inicializaremos y configuraremos nuestra aplicación Flask
- Centraliza la configuración de la app (base de datos, blueprints, etc.)

**Concepto clave:** Sin `__init__.py`, Python no reconocería `todor` como un paquete importable.
'''