from src.controllers.private import *

private = {
    "private_route": "/panel", "private_controller": PrivateController.as_view("private"),
    "config_route": "/config", "config_controller": ConfigurationController.as_view("config"),
    
    #user routes.
    "user-edit_route": "/edit/user/<string:identity>", "user-edit_controller": UserController.as_view("user-edit"),
    "logout_route": "/logout", "logout_controller": LogoutController.as_view("logout"),
    "register_route": "/register", "register_controller": RegisterController.as_view("register"),
    
    #Excel file.
    "load_route": "/load", "load_controller": FileController.as_view("load"),
    
    #Products routes.
    "add-products_route": "/add/products", "add-products_controller": AddProductsController.as_view("add-products"),
}