from flask.views import MethodView
from flask import redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash
from src.db import mysql

class SigninController(MethodView):
    def get(self):
        if("username" in session):
            return redirect('/panel')
        return render_template('public/auth.html')
    
    def post(self):
        if("username" in session):
            return redirect('/panel')
        email = request.form['email']
        password = request.form['password']
        global user
        with mysql.cursor() as cur:
            try:
                cur.execute("SELECT * FROM users WHERE email = %s", (email))
                user = cur.fetchone()
                if not check_password_hash(user[5], password):
                    flash("La contraseña es incorrecta")
                    return redirect('/')
                if(user):
                    session.clear()
                    session['user_id'] = user[0]
                    session['username'] = user[2]
                    session['role'] = user[6]
                    flash("El usuario {0} ha iniciado sesión".format(user[2]))
                    return redirect('/panel')
            except:
                flash("Los datos son erróneos.")
            flash("El email o la contraseña son incorrectos")
            return redirect('/')