from src.controllers.private import *

private = {
    "private_route": "/panel", "private_controller": PrivateController.as_view("private"),
    "config_route": "/config", "config_controller": ConfigurationController.as_view("config"),
    "register_route": "/register", "register_controller": RegisterController.as_view("register"),
    "logout_route": "/logout", "logout_controller": LogoutController.as_view("logout"),
    
    #user routes.
    "user-edit_route": "/edit/user/<string:identity>", "user-edit_controller": UserController.as_view("user-edit"),
    
    #Excel file.
    "load_route": "/load", "load_controller": FileController.as_view("load")
}