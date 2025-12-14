from main import db

class User(db.Model): #El nombre de la clase representa el nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key = True) #Cada atributo representa la columna en la base de datos
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)

    def __init__(self, username, password): #Esto sirve para crear objetos de la clase User
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<User: {self.username}>'

