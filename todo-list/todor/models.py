'''
**¿Qué contiene?** Las **clases que representan las tablas de la base de datos**.

**Ejemplo de lo que contendrá:**
```python
# Clase que representa la tabla 'users' en la base de datos
class User:
    id
    username
    email
    password
    
# Clase que representa la tabla 'todos' en la base de datos  
class Todo:
    id
    title
    description
    completed
    user_id  # Relación con User
```

**¿Por qué es importante?** Define la estructura de datos de tu aplicación.  Estos modelos se convertirán en tablas de la base de datos usando un ORM (Object-Relational Mapping) como SQLAlchemy.
'''