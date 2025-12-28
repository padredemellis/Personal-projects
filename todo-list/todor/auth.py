from flask import Blueprint, render_template
from . import models
'''
**¿Qué contiene?** Toda la lógica de **autenticación de usuarios**.

**Ejemplos de rutas que irán aquí:**
- `GET /register` - Mostrar formulario de registro
- `POST /register` - Procesar registro de nuevo usuario
- `GET /login` - Mostrar formulario de login
- `POST /login` - Procesar inicio de sesión
- `GET /logout` - Cerrar sesión

**Concepto clave:** Maneja todo lo relacionado con la identidad del usuario (quién es, puede acceder, etc.).
'''
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register')
def register():
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')