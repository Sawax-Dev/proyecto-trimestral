from src.controllers.public import *
from src.controllers.errors import *

public = {
    "signin_route": "/", "signin_controller": SigninController.as_view("signin"),
    "not_found_route": 404, "not_found_controller": NotFoundController.as_view("not_found")
}