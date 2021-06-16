from flask import redirect, session, flash

def role_required(view):
    def required(paramView, identity=None):
        if(session['role'] != 'Administrador'):
            flash("Sin autorización para acceder a la vista")
            return redirect('/panel')
        return view(paramView)
    return required