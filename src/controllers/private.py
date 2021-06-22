from flask.views import MethodView
from flask import request, render_template, redirect, session, flash
from werkzeug.security import generate_password_hash
from src.db import mysql
from src.hooks.roleRequired import role_required
from src.hooks.loginRequired import login_required
from src.services.file_service import FileService

class PrivateController(MethodView):
    @login_required
    def get(self):
        user = session["username"]
        return render_template('private/panel.html', user=user)

class ConfigurationController(MethodView):
    @login_required
    def get(self):
        with mysql.cursor() as cur:
            try:
                cur.execute("SELECT identity, name, id_type, last_name, email, role FROM users")
                users = cur.fetchall()
            except:
                flash("Ha ocurrido un error mientras intentabamos mostrar los datos")
            return render_template('private/config.html', users=users)
    
    @login_required
    def post(self):
        return "Configurations post works!"

#
class FileController(MethodView):
    
    __fileSvc = FileService()
    
    def get(self):
        pass
    
    @login_required
    @role_required
    def post(self):
        file = self.__fileSvc.load()
        if file is None:
            flash("Ocurrió un error al mostrar la carga de los datos del archivo")
            return redirect('/config')
        return f"{file}"

class UserController(MethodView):
    def get(self, identity):
        if("username" not in session):
            flash("Primero debe iniciar sesión")
            return redirect('/')
        elif("Administrador" not in session['role']):
            flash("Sin autorización para acceder a la vista")
            return redirect('/config')
        with mysql.cursor() as cur:
            try:
                cur.execute("SELECT * FROM users WHERE identity = %s", (identity))
                user = cur.fetchone()
            except:
                flash("Ha ocurrido un error mientras intentabamos mostrar los datos")
            return render_template('private/user-edit.html', user=user)
    
    def post(self, identity):
        if("username" not in session):
            flash("Primero debe iniciar sesión")
            return 
        elif("Administrador" not in session['role']):
            flash("Sin autorización para acceder a la vista")
            return redirect('/config')
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']
        id_type = request.form['id_type']
        with mysql.cursor() as cur:
            try:
                cur.execute("UPDATE users SET name = %s, last_name = %s, email = %s, id_type = %s WHERE identity = %s", (name, last_name, email, id_type, identity))
                mysql.commit()
            except:
                flash("Ha ocurrido un error mientras intentabamos actualizar los datos")
            flash("Se han actualizado los datos del usuario")
            return redirect('/config')

class RegisterController(MethodView):
    @login_required
    @role_required
    def get(self):
        return render_template('private/register.html')
    
    @login_required
    @role_required
    def post(self):
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        id_type = request.form['id_type']
        identity = request.form['identity']
        role = request.form['role']
        with mysql.cursor() as cur:
            try:
                query = cur.execute("SELECT identity FROM users WHERE email = %s", (email))
            except:
                flash("ocurrió un error mientras intentabamos registrar el usuario")
            if(query):
                flash("El email ya existe en la base de datos")
                return redirect('/register')
            elif(len(password) < 8):
                flash("La contraseña escrita es muy corta")
                return redirect('/register')
            try:
                cur.execute("INSERT INTO users(identity, name, id_type, last_name, email, password, role) VALUES(%s, %s, %s, %s, %s, %s, %s)", (identity, name, id_type, last_name, email, generate_password_hash(password), role))
                mysql.commit()
            except:
                flash("ocurrió un error mientras intentabamos registrar el usuario")
            finally:
                cur.close()
                mysql.close()
            flash("Se ha registrado el usuario en la base de datos")
            return redirect('/panel')

class LogoutController(MethodView):
    @login_required
    def get(self):
        session.clear()
        flash("La session ha sido cerrada")
        return redirect('/')