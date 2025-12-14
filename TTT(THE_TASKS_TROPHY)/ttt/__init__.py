from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # Creamos una instancia de la base de datos en db

def create_app(): 
    app = Flask(__name__)
    #Configuracion del proyecto
    app.config.from_mapping(
        DEBUG= True,
        SCRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///The_task_trophy.db"
    )

    db.init_app(app) #Metodo para inicializar la conoeccion a nuestra base de datos
    
    #Registrar Blueprint
    from . import main
    app.register_blueprint(main.bp)
    
    from . import auth
    app.register_blueprint (auth.bp)


    @app.route('/')
    def index():
        return render_template('index.html')
    
    with app.app_context(): #Esto migra todos los modelos que van a haber en nuestra aplicacion a la base de datos
        db.create_all()

    return app


