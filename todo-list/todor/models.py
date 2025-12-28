'''
**¿Qué contiene?** Las **clases que representan las tablas de la base de datos**.
**¿Por qué es importante?** Define la estructura de datos de tu aplicación.  Estos modelos se convertirán en tablas de la base de datos usando un ORM (Object-Relational Mapping) 
'''

from todor import db
# Clase que representa la tabla 'users' en la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False) # va a ser un valor unico y no va a aceptar un valor nulo
    password = db.Column(db.Text, nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f"<User: {self.username >}"  #representamos por el nombre de usuario
# Clase que representa la tabla 'todos' en la base de datos  
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # relacion para que usuario pueda tener varias tareas, la clase es User en mayusdcula pero se migrará en minuscula por eso va en minuscula
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text)
    state = db.Column(db.Boolean, default = False)

    def __init__(self, created_by, title, description, state = False):
        self.created_by = created_by
        self.title = title
        self.description = description
        self.state = state

    def __repr__(self):
        return f"<Todo: {self.title} >"
        
