from ttt import db

class User(db.Model): #El nombre de la clase representa el nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key = True) #Cada atributo representa la columna en la base de datos
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)

    def __init__(self, username, password): #Esto sirve para crear objetos de la clase User
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<User: {self.username}>'

class Ttt(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) 
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text)
    state = db.Column(db.Boolean, default = False)

    def __init__(self, created_by, title, description, state = False): 
        self.created_by = created_by
        self.title = title
        self.description = description
        self.state = state

    
    def __repr__(self):
        return f'<The task trophy: {self.title}>'

 