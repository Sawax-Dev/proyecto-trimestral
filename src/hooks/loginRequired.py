from flask import redirect, session, flash

def login_required(view):
    def required(finalView):
        if("username" not in session):
            flash("Por favor, debes iniciar sesión")
            return redirect('/')
        return view(finalView)
    return required