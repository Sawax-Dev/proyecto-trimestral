from flask import Flask
from src.routes.public import *
from src.routes.private import *

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = 'asdasjnwjasdm,asd'
)

"""
    Public routes
"""
#Signin route.
app.add_url_rule(public["signin_route"], view_func=public["signin_controller"])

"""
    Private routes
"""
app.add_url_rule(private["private_route"], view_func=private["private_controller"])
app.add_url_rule(private["config_route"], view_func=private["config_controller"])
app.add_url_rule(private["register_route"], view_func=private["register_controller"])
app.add_url_rule(private["logout_route"], view_func=private["logout_controller"])

#User routes
app.add_url_rule(private["user-edit_route"], view_func=private["user-edit_controller"])

#Excel file route.
app.add_url_rule(private["load_route"], view_func=private["load_controller"])
""" 
    Handle erros.
"""
app.register_error_handler(public["not_found_route"], public["not_found_controller"])