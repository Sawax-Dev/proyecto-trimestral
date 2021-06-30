from src.controllers.private import *

private = {
    "private_route": "/panel", "private_controller": PanelController.as_view("private"),
    "panel-delete_route": "/panel/delete/<int:id>", "panel-delete_controller": PanelDeleteController.as_view("panel-delete"),
    "invoicing_route": "/invoicing/<string:uid>", "invoicing_controller": InvoicingController.as_view("invoicing"),
    
    "config_route": "/config", "config_controller": ConfigurationController.as_view("config"),
    
    #Invoices routes.
    "invoices-list_route": "/invoices", "invoices-list_controller": InvoicesListController.as_view("invoices-list"),
    
    #user routes.
    "user-list_route": "/users", "user-list_controller": UsersListController.as_view("user-list"),
    "user-edit_route": "/edit/user/<string:identity>", "user-edit_controller": UserEditController.as_view("user-edit"),
    "logout_route": "/logout", "logout_controller": LogoutUserController.as_view("logout"),
    "register_route": "/register", "register_controller": RegisterUserController.as_view("register"),
    
    #Customers routes.
    "customer-add_route": "/customer/add", "customer-add_controller": CustomersAddController.as_view("customer-add"),
    
    #Excel file.
    "load_route": "/load", "load_controller": FileController.as_view("load"),
    
    #Products routes.
    "add-products_route": "/add/products", "add-products_controller": ProductsAddController.as_view("add-products"),
    "products-list_route": "/products", "products-list_controller": ProductsListController.as_view("products-list"),
    "products-edit_route": "/edit/product/<int:code>", "products-edit_controller": ProductsEditController.as_view("products-edit"),
    
    #Categories routes.
    "categories-list_route": "/categories", "categories-list_controller": CategoriesListController.as_view("categories-list"),
    "categories-add_route": "/categories/add", "categories-add_controller": CategoriesAddController.as_view("categories-add"),
    
}