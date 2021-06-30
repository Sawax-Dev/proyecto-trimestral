from flask.views import MethodView
from flask import request, render_template, redirect, session, flash
from werkzeug.security import generate_password_hash
from src.db import mysql
from src.hooks.roleRequired import role_required
from src.hooks.loginRequired import login_required
from src.services.file_service import FileService

class PanelController(MethodView):
    @login_required
    def get(self):
        with mysql.cursor() as cur:
            data = []
            details = []
            invoice = []
            try:
                cur.execute(f"SELECT number, current_money, base FROM cash_register INNER JOIN users ON cash_register.number = users.register_number WHERE users.identity = '{session['user_id']}'")
                data = cur.fetchone()
                if(data):
                    session['user_register_number'] = data[0]
                    session['user_base'] = data[2]
                cur.execute(f"SELECT id, code, name, unit_value, quantity FROM products INNER JOIN cart_tmp ON products.code = cart_tmp.product")
                details = cur.fetchall()
                if('customer' in session):
                    cur.execute(f"SELECT uid FROM invoices WHERE customer = '{session['customer']}'")
                    invoice = cur.fetchone()
            except Exception as e:
                flash(f'{e}', 'error')
            return render_template('private/panel.html', data=data, details=details, invoice=invoice)
    
    @login_required
    def post(self):
        #Add product to invoices_details.
        code = request.form['productCode']
        quantity: int = int(request.form['productQuantity'])
        if quantity < 1:
            flash('La cantidad del producto no puede ser menor que uno (1)', 'error')
            return redirect(request.url)
        
        with mysql.cursor() as cur:
            productData = []
            invoice = []
            try:
                cur.execute("SELECT * FROM products WHERE code = %s", (code))
                productData = cur.fetchone()
                if(not productData):
                    flash('No se encontraron productos con el código ingresado', 'error')
                    return redirect(request.url)
                if('customer' in session):
                    cur.execute(f"SELECT uid FROM invoices WHERE customer = '{session['customer']}'")
                    invoice = cur.fetchone()
                    cur.execute("INSERT INTO cart_tmp(product, invoice, quantity, unit_value, total_iva) VALUES(%s, %s, %s, %s, %s)", (productData[0], invoice[0], quantity, productData[3], productData[4]))
                    mysql.commit()
                    cur.execute("UPDATE products SET stock = %s WHERE code = %s", (productData[2]-quantity, code))
                    flash('El producto ha sido añadido al carrito de compras.', 'success')
                else:
                    flash('Primero debe ingresar un comprador.', 'error')
            except Exception as e:
                flash(f"{e}", "error")
            return redirect('/panel')

class InvoicingController(MethodView):
    #@login_required
    def get(self, uid):
        with mysql.cursor() as cur:
            invoiceData = []
            sellerData = []
            details = []
            try:
                cur.execute("SELECT * FROM invoices INNER JOIN customers WHERE invoices.uid = %s", (uid))
                invoiceData = cur.fetchone()
                cur.execute("SELECT identity, name, last_name, number, base FROM users INNER JOIN cash_register WHERE users.identity = %s", (session.get('user_id')))
                sellerData = cur.fetchone()
                cur.execute(f"SELECT id, code, name, unit_value, quantity, total_iva FROM products INNER JOIN cart_tmp ON products.code = cart_tmp.product")
                details = cur.fetchall()
                cur.execute(f"SELECT SUM(unit_value*quantity) FROM cart_tmp")
                total_value = cur.fetchone()
                cur.execute(f"SELECT SUM((unit_value * total_iva * quantity) / 100) FROM cart_tmp")
                iva = cur.fetchone()
            except Exception as e:
                flash("Un error se ha generado durante la consulta de datos", "error")
            return render_template('private/invoicing.html', invoiceData=invoiceData, sellerData=sellerData, details=details, value=total_value, iva=iva)
    
    #@login_required
    def post(self, uid):
        payment_type = request.form['payment_type']
        total_value = float(request.form['total'])
        customer_pay = float(request.form['customer_pay'])
        refund = float(request.form['devuelta'])
        print(payment_type, total_value, customer_pay, refund)
        
        with mysql.cursor() as cur:
            try:
                if(payment_type == 'efectivo'):
                    pass
                else:
                    pass
                cur.execute(f"SELECT invoice, product, quantity, unit_value, total_iva FROM cart_tmp WHERE invoice = '{uid}'")
                invoice_details = cur.fetchall()
                for i in invoice_details:
                    cur.execute("INSERT INTO invoices_details(invoice, product, quantity, unit_value, total_iva, payment) VALUES(%s, %s, %s, %s, %s, %s)", (i[0], i[1], i[2], i[3], i[4], payment_type))
                    mysql.commit()
                cur.execute("SELECT SUM(unit_value * quantity) FROM invoices_details WHERE invoice = %s", (uid))
                total = cur.fetchone()
                cur.execute("SELECT SUM((unit_value * total_iva * quantity) / 100) FROM invoices_details WHERE invoice = %s", (uid))
                iva = cur.fetchone()
                cur.execute("UPDATE invoices SET total_value = %s, total_iva = %s WHERE uid = %s", (total, iva, uid))
                mysql.commit()
                cur.execute("UPDATE cash_register SET current_money += %s WHERE number = %s", (total_value-refund, session['user_register_number']))
                mysql.commit()
                if(invoice_details):
                    cur.execute("DELETE FROM cart_tmp WHERE invoice = %s", (uid))
                    mysql.commit()
                flash('La facturación se ha realizado correctamente', 'success')
            except Exception as e:
                flash(f"{e}", "error")
            return redirect('/panel')

class CloseBoxController(MethodView):
    @login_required
    @role_required
    def post(self):
        date = request.form['date']
        
        with mysql.cursor() as cur:
            sell_value = []
            total = []
            try:
                #Efectivo.
                cur.execute(f"SELECT payment FROM invoices_details WHERE payment = 1")
                payment_type = cur.fetchall()
                if(payment_type):
                    cur.execute(f"SELECT SUM(total_value + total_iva) FROM invoices WHERE date LIKE '%{date}%'")
                    sell_value = cur.fetchone()
                #Total de todo.
                cur.execute(f"SELECT SUM(total_value + total_iva) FROM invoices WHERE date LIKE '%{date}%'")
                total = cur.fetchone()
                print(total)
            except Exception as e:
                flash(f"{e}", "error")
            return render_template('private/close.html', sell_value=sell_value, total=total)

class PanelDeleteController(MethodView):
    def post(self, id):
        with mysql.cursor() as cur:
            try:
                cur.execute("DELETE FROM cart_tmp WHERE id = %s", (id, ))
                mysql.commit()
                flash("El producto se ha eliminado del carrito.", "success")
            except Exception as e:
                flash("Un error ha ocurrido mientras intentabamos borrar el producto del carrito.", "error")
        return redirect('/panel')

class CustomersAddController(MethodView):
    @login_required
    def post(self):
        #Add customer.
        id = request.form['id']
        idType = request.form['id_type']
        phone = request.form['phone']
        name = request.form['name']
        last_name = request.form['last_name']
        
        #Invoices
        invoice_uid = request.form['invoice']
        seller = session.get('user_id')
        
        with mysql.cursor() as cur:
            try:
                cur.execute("INSERT INTO customers VALUES(%s, %s, %s, %s, %s)", (id, name, last_name, idType, phone))
                mysql.commit()
                cur.execute("INSERT INTO invoices(uid, seller, customer) VALUES(%s, %s, %s)", (invoice_uid, seller, id))
                mysql.commit()
                session['invoice'] = invoice_uid
                session['customer'] = id
                flash(f'El comprador ha sido agregado. Código de factura. {invoice_uid}', 'success')
            except Exception as e:
                flash(f"{e}", "error")
            return redirect('/panel')

#Invoices controller.
class InvoicesListController(MethodView):
    @login_required
    def get(self):
        with mysql.cursor() as cur:
            invoices = []
            try:
                cur.execute("SELECT invoices.*, users.name, users.last_name, users.role FROM invoices INNER JOIN users ON invoices.seller = users.identity")
                invoices = cur.fetchall()
                cur.execute("SELECT name, last_name FROM invoices INNER JOIN customers ON invoices.customer = customers.id")
                customers = cur.fetchall()
            except Exception as e:
                flash(f"{e}", "error")
            return render_template('private/invoices/list.html', invoices=invoices, customers=customers)
    
    @login_required
    def post(self):
        search = request.form['search']
        date_start = request.form['date_start']
        date_end = request.form['date_end']
        print(date_start, date_end)
        
        with mysql.cursor() as cur:
            try:
                cur.execute(f"SELECT invoices.*, users.name, users.last_name, users.role FROM invoices INNER JOIN users ON invoices.seller = users.identity WHERE invoices.date BETWEEN '{date_start}' AND '{date_end}'")
                resultByDateToDate = cur.fetchall()
                if(resultByDateToDate):
                    flash(f"Los resultados desde {date_start} hasta {date_end} son...", "success")
                    return render_template('private/invoices/list.html', invoices=resultByDateToDate)
                cur.execute(f"SELECT invoices.*, users.name, users.last_name, users.role FROM invoices INNER JOIN users ON invoices.seller = users.identity WHERE users.name LIKE'%{search}%'")
                result = cur.fetchall()
                if(result):
                    flash(f"Los resultados de la búsqueda por el vendedor {search} son...", "success")
                    return render_template('private/invoices/list.html', invoices=result)
                cur.execute(f"SELECT invoices.*, users.name, users.last_name, users.role FROM invoices INNER JOIN users ON invoices.seller = users.identity WHERE invoices.date LIKE'%{search}%'")
                resultByDate = cur.fetchall()
                if(resultByDate):
                    flash(f"Los resultados de la búsqueda por la fecha {search} son...", "success")
                    return render_template('private/invoices/list.html', invoices=resultByDate)
            except Exception as e:
                flash(f"{e}", "error")
            flash("No se encontraron resultados..", "error")
            return redirect('/invoices')

#End invoices controller.

#TODO://ERROR PARA RESOLVER EN MÉTODO GET
class ConfigurationController(MethodView):
    @login_required
    def get(self):
        user = []
        with mysql.cursor() as cur:
            try:
                cur.execute(f"SELECT name, last_name, role FROM users WHERE identity = {session['user_id']}")
                user = cur.fetchone()
            except Exception as e:
                flash(f'{e}', 'error')
            return render_template('private/config.html', user=user)

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
                values = (value[0], value[1], value[2], value[3], value[4], value[5], value[6])
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
class UsersListController(MethodView):
    @login_required
    @role_required
    def get(self):
        users = []
        with mysql.cursor() as cur:
            try:
                cur.execute("SELECT identity, name, id_type, last_name, email, role, created_at, register_number FROM users")
                users = cur.fetchall()
            except Exception as e:
                flash(f'{e}', 'error')
            return render_template('private/users/user-list.html', users=users)
    
    @login_required
    @role_required
    def post(self):
        search = request.form['search']
        with mysql.cursor() as cur:
            try:
                cur.execute(f"SELECT identity, name, id_type, last_name, email, role FROM users WHERE name LIKE'%{search}%'")
                results = cur.fetchall()
                if(results):
                    flash(f'A continuación te mostramos los resultados de la búsqueda {search}...', 'success')
                    return render_template('private/users/user-list.html', users=results, user=[session['username'], 'Undefined', session['role']])
            except Exception as e:
                flash('{0}', 'error'.format(e))
            flash('No se encontraron resultados', 'error')
            return redirect('/users')

class UserEditController(MethodView):
    def get(self, identity):
        if("username" not in session):
            flash("Primero debe iniciar sesión.", "error")
            return redirect('/')
        elif("Administrador" not in session['role']):
            flash("Sin autorización para acceder a la vista.", "error")
            return redirect('/')
        user = []
        cashInfo = []
        with mysql.cursor() as cur:
            try:
                #cur.execute(f"SELECT users.*, base FROM users INNER JOIN cash_register ON users.register_number = cash_register.number WHERE identity = {identity}")
                cur.execute("SELECT identity, id_type, name, last_name, email, role, register_number FROM users WHERE identity = %s", (identity))
                user = cur.fetchone()
                cur.execute(f"SELECT number FROM cash_register")
                cashInfo = cur.fetchall()
            except Exception as e:
                flash("{0}", "error".format(e))
            return render_template('private/users/user-edit.html', user=user, cashInfo=cashInfo)
    
    def post(self, identity):
        if("username" not in session):
            flash("Primero debe iniciar sesión.", "error")
            return redirect('/')
        elif("Administrador" not in session['role']):
            flash("Sin autorización para acceder a la vista.", "error")
            return redirect('/')
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']
        id_type = request.form['id_type']
        register_number = request.form['register_number']
        with mysql.cursor() as cur:
            try:
                cur.execute(f"UPDATE users SET id_type = '{id_type}', name = '{name}', last_name = '{last_name}', email = '{email}', register_number = {register_number} WHERE identity = '{identity}'")
                mysql.commit()
                #session['username'] = name
                #session['user_register_number'] = register_number
            except Exception as e:
                flash("{0}", "Error".format(e))
            flash("Se han actualizado los datos del usuario.", "success")
            return redirect('/users')

class RegisterUserController(MethodView):
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

class LogoutUserController(MethodView):
    @login_required
    def get(self):
        session.clear()
        flash("La session ha sido cerrada.", "success")
        return redirect('/')
#End users controllers

#Products controllers
class ProductsAddController(MethodView):
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

class ProductsListController(MethodView):
    @login_required
    @role_required
    def get(self):
        with mysql.cursor() as cur:
            categories = {
                "food": [],
                "drinks": [],
                "cleaning": [],
                "some": []
            }
            try:
                cur.execute("SELECT code, name, stock, value, iva, expiration_date FROM products WHERE category = 1 ORDER BY name ASC")
                categories['food'] = cur.fetchall()
                cur.execute("SELECT code, name, stock, value, iva, expiration_date FROM products WHERE category = 2 ORDER BY name ASC")
                categories['drinks'] = cur.fetchall()
                cur.execute("SELECT code, name, stock, value, iva, expiration_date FROM products WHERE category = 3 ORDER BY name ASC")
                categories['cleaning'] = cur.fetchall()
                cur.execute("SELECT code, name, stock, value, iva, expiration_date FROM products WHERE category = 4 ORDER BY name ASC")
                categories['some'] = cur.fetchall()
            except Exception as e:
                flash("Un error se ha generado durante la consulta", "error")
            return render_template('private/products/list.html', food=categories['food'], drinks=categories['drinks'], cleanings=categories['cleaning'], some=categories['some'])
    
    @login_required
    @role_required
    def post(self):
        pass

class ProductsEditController(MethodView):
    def get(self, code):
        if("username" not in session):
            flash("Primero debe iniciar sesión.", "error")
            return redirect('/')
        elif("Administrador" not in session['role']):
            flash("Sin autorización para acceder a la vista.", "error")
            return redirect('/')
        product = []
        with mysql.cursor() as cur:
            try:
                cur.execute("SELECT code, name, stock, value, iva, discount, category, expiration_date FROM products WHERE code = %s", (code))
                product = cur.fetchone()
            except Exception as e:
                flash("Un error ocurrió mientras se consultaban los datos", "error")
            return render_template('private/products/edit.html', product=product)
    
    def post(self, code):
        if("username" not in session):
            flash("Primero debe iniciar sesión.", "error")
            return redirect('/')
        elif("Administrador" not in session['role']):
            flash("Sin autorización para acceder a la vista.", "error")
            return redirect('/')
        codeForm = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']
        iva = request.form['iva']
        category = request.form['category']
        expiration_date = request.form['expiration_date']
        discount = request.form['discount']
        with mysql.cursor() as cur:
            try:
                cur.execute(f"UPDATE products SET code = {codeForm}, name = '{name}', stock = {stock}, value = {value}, iva = {iva}, category = {category}, expiration_date = '{expiration_date}', discount = {discount} WHERE code = {code}")
                mysql.commit()
                flash('Los datos del producto se han actualizado correctamente', 'success')
            except Exception as e:
                flash("Ocurrió un error durante la actualización de los datos", "error")
            return redirect('/products')
#End products controllers

#Categories controllers.
class CategoriesListController(MethodView):
    @login_required
    @role_required
    def get(self):
        return render_template('private/categories/list.html')

class CategoriesAddController(MethodView):
    @login_required
    @role_required
    def post(self):
        pass
#End categories controllers