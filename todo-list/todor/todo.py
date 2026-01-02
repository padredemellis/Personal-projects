from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from todor.auth import login_required
from .models import Todo, User
from todor import db
'''
**Desglose de cada importación:**
- `Blueprint` → Para crear el blueprint
- `render_template` → Para renderizar plantillas HTML
- `request` → Para acceder a datos del formulario y de la petición
- `redirect` → Para redirigir a otras rutas
- `url_for` → Para generar URLs dinámicamente
- `flash` → Para mostrar mensajes temporales al usuario
- `session` → Para manejar datos de sesión del usuario
'''

bp = Blueprint('todo', __name__, url_prefix='/todo')

@bp.route('/list')
@login_required
def index():
    todos = Todo.query.all()
    return render_template("todo/index.html", todos = todos)

@bp.route('/create')
def create():
    return "Crear tareas"


















'''
**¿Qué contiene?** Todas las **rutas (views)** relacionadas con las tareas (todos).

**Ejemplos de rutas que irán aquí:**
- `GET /todos` - Ver todas las tareas
- `POST /todos/create` - Crear nueva tarea
- `PUT /todos/<id>/update` - Actualizar una tarea
- `DELETE /todos/<id>/delete` - Eliminar una tarea

**¿Por qué separar las vistas?** Organización y escalabilidad.  En aplicaciones grandes, cada módulo maneja su propia área de funcionalidad.
'''