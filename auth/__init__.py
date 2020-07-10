from flask import g, request, Response
import settings
import importlib
from functools import wraps
import os

def login_required(auth_method_path=None):
    def login_required_decorator(wrapped):
        @wraps(wrapped)
        def wrapper(*args, **kwargs):
            if isinstance(auth_method_path, str):
                authenticate = get_authenticator(auth_method_path)
            else:
                authenticate = get_authenticator()
            if authenticate():
                return wrapped(*args, **kwargs)

            return Response("Forbidden", 403)

        return wrapper

    if callable(auth_method_path):
        # If the decorator is used w/out any arguments,
        # `auth_method_path` won't reference the path to the
        # authentication method. Instead, it will reference
        # the method being wrapped. Hence the 'callable' check.
        return login_required_decorator(auth_method_path)
    
    return login_required_decorator

def get_authenticator(auth_method_path=None):
    if auth_method_path:
        pass
    elif os.environ.get("AUTHENTICATION_METHOD_PATH"):
        auth_method_path = os.environ.get("AUTHENTICATION_METHOD_PATH")
    elif settings.authentication_method_path:
        auth_method_path = settings.authentication_method_path
    else:
        raise Exception()

    path_pieces = auth_method_path.split(".")
    module = importlib.import_module(".".join(path_pieces[:-1]))
    return getattr(module, path_pieces[-1])