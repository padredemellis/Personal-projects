from flask import (
    Blueprint, render_template, request, url_for, redirect, flash
    )

from werkzeug.security import generate_password_hash, check_password_hash


from .models import User
from ttt import db

bp = Blueprint('auth', __name__, url_prefix = "/auth")

@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username, generate_password_hash(password))

        error = None

        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f' El usuario {username} ya esta registrado'
        
        flash(error)
    return render_template("auth/register.html")

@bp.route('/login')
def login():
    return render_template("auth/login.html")