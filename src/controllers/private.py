from flask.views import MethodView
from flask import request, render_template, redirect, session, flash
from werkzeug.security import generate_password_hash
from src.db import mysql
from src.hooks.roleRequired import role_required
from src.hooks.loginRequired import login_required
from src.services.file_service import FileService

#Panel/loading page controller.
#TODO://ERROR PARA RESOLVER EN CONSULTA SQL.
class PrivateController(MethodView):
    @login_required
    def get(self):
        data = []
        with mysql.cursor() as cur:
            try:
                cur.execute(f"SELECT number, base FROM cash_register INNER JOIN users ON cash_register.number = users.register_number WHERE users.identity = {session['user_id']}")
                data = cur.fetchone()
                if(data):
                    session['user_register_number'] = data[0]
                    session['user_base'] = data[1]
            except Exception as e:
                flash(f'{e}', 'error')
            return render_template('private/panel.html', data=data)

#TODO://ERROR PARA RESOLVER EN MÉTODO GET
class ConfigurationController(MethodView):
    @login_required
    def get(self):
        user = []
        users = []
        with mysql.cursor() as cur:
            try:
                cur.execute("SELECT identity, name, id_type, last_name, email, role FROM users")
                users = cur.fetchall()
                cur.execute(f"SELECT name, last_name, role FROM users WHERE identity = {session['user_id']}")
                user = cur.fetchone()
            except Exception as e:
                flash(f'{e}', 'error')
            return render_template('private/config.html', users=users, user=user)
    
    @login_required
    def post(self):
        search = request.form['search']
        with mysql.cursor() as cur:
            try:
                cur.execute(f"SELECT identity, name, id_type, last_name, email, role FROM users WHERE name LIKE'%{search}%'")
                results = cur.fetchall()
                if(results):
                    flash(f'A continuación te mostramos los resultados de la búsqueda {search}...', 'success')
                    return render_template('private/config.html', users=results, user=[session['username'], 'Undefined', session['role']])
            except Exception as e:
                flash('{0}', 'error'.format(e))
            flash('No se encontraron resultados', 'error')
            return redirect('/config')

class FileController(MethodView):
    
    __fileSvc = FileService()
    
    @login_required
    @role_required
    def get(self):
        error: str = None
        file = self.__fileSvc.load()
        if file is None:
            flash("No se encontraron datos en el archivo Excel.", "error")
            return redirect('/config')
        with mysql.cursor() as cur:
            for value in file:
                data: list = value
                values = (data[0], data[1], data[2], data[3], data[4], data[5], data[6])
                try:
                    cur.execute("INSERT INTO products(code, name, stock, value, iva, category, expiration_date) VALUES(%s, %s, %s, %s, %s, %s, %s)", (values))
                    cur.connection.commit()
                except Exception as e:
                    error = "{0}".format(e)
            if error is None:
                flash("Los datos de Excel se han cargado en la base de datos", "success")
            else:
                flash(error, "error")
            return redirect('/')

#Users controller
class UserController(MethodView):
    def get(self, identity):
        if("username" not in session):
            flash("Primero debe iniciar sesión.", "error")
            return redirect('/')
        elif("Administrador" not in session['role']):
            flash("Sin autorización para acceder a la vista.", "error")
            return redirect('/config')
        with mysql.cursor() as cur:
            try:
                #cur.execute("SELECT * FROM users WHERE identity = %s", (identity))
                cur.execute(f"SELECT users.*, base FROM users INNER JOIN cash_register ON users.register_number = cash_register.number WHERE identity = {identity}")
                user = cur.fetchone()
                cur.execute(f"SELECT number, base, date FROM cash_register")
                cashInfo = cur.fetchall()
                #print(cashInfo)
            except Exception as e:
                flash("{0}", "error".format(e))
            return render_template('private/users/user-edit.html', user=user, cashInfo=cashInfo)
    
    def post(self, identity):
        if("username" not in session):
            flash("Primero debe iniciar sesión.", "error")
            return 
        elif("Administrador" not in session['role']):
            flash("Sin autorización para acceder a la vista.", "error")
            return redirect('/config')
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']
        id_type = request.form['id_type']
        register_number = request.form['register_number']
        base = request.form['base']
        print(register_number)
        with mysql.cursor() as cur:
            try:
                cur.execute("UPDATE users SET name = %s, last_name = %s, email = %s, id_type = %s, register_number = %s WHERE identity = %s", (name, last_name, email, id_type, register_number, identity))
                cur.connection.commit()
                cur.execute("UPDATE cash_register SET base = %s WHERE number = %s", (base, session['user_register_number']))
                cur.connection.commit()
                session['username'] = name
                session['user_register_number'] = register_number
                session['user_base'] = base
            except Exception as e:
                flash("{0}", "Error".format(e))
            flash("Se han actualizado los datos del usuario.", "success")
            return redirect('/config')

class RegisterController(MethodView):
    @login_required
    @role_required
    def get(self):
        return render_template('private/users/user-register.html')
    
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
            except Exception as e:
                flash("{0}", "error".format(e))
            if(query):
                flash("El email ya existe en la base de datos.", "error")
                return redirect('/register')
            elif(len(password) < 8):
                flash("La contraseña escrita es muy corta.", "error")
                return redirect('/register')
            try:
                cur.execute("INSERT INTO users(identity, name, id_type, last_name, email, password, role) VALUES(%s, %s, %s, %s, %s, %s, %s)", (identity, name, id_type, last_name, email, generate_password_hash(password), role))
                mysql.commit()
            except Exception as e:
                flash("{0}", "error".format(e))
            flash("Se ha registrado el usuario en la base de datos.", "success")
            return redirect('/panel')

class LogoutController(MethodView):
    @login_required
    def get(self):
        session.clear()
        flash("La session ha sido cerrada.", "success")
        return redirect('/')
#End users controllers

class AddProductsController(MethodView):
    @login_required
    @role_required
    def get(self):
        categories = []
        with mysql.cursor() as cur:
            try:
                cur.execute("SELECT code, name FROM category")
                categories = cur.fetchall()
            except Exception as e:
                flash('{0}', 'error'.format(e))
            return render_template('private/products/add.html', categories=categories)
    
    @login_required
    @role_required
    def post(self):
        code = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']
        iva = request.form['iva']
        category = request.form['category']
        expiration_date = request.form['expiration_date']
        if(float(value) < 101 and float(value) >= 9999999):
            flash('El valor debe estar entre 100 y 9999999.', "error")
            return redirect('/add/products')
        data: tuple = (code, name, stock, value, iva, category, expiration_date)
        with mysql.cursor() as cur:
            try:
                cur.execute("INSERT INTO products(code, name, stock, value, iva, category, expiration_date) VALUES(%s, %s, %s, %s, %s, %s, %s)", (data))
                cur.connection.commit()
                flash("El producto ha sido agregado satisfactoriamente", "success")
            except Exception as e:
                flash("{0}", 'error'.format(e))
            return redirect('/')